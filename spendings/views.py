from rest_framework import viewsets
from rest_framework.response import Response

from spendings.serializers import SpendingsSerializer
from spendings.models import Spendings


class SpendingsViewSet(viewsets.ModelViewSet):
    serializer_class = SpendingsSerializer

    def get_queryset(self):
        spendings = Spendings.objects.order_by('amount').all()
        currency = self.request.query_params.get('currency')
        
        if currency:
            spendings = spendings.filter(currency=currency)

        return spendings

    def delete(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        instance = self.get_object(pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')

        serializer = SpendingsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = Spendings.objects.filter(pk=pk).first() 
        instance.amount = request.data.get('amount')
        instance.currency = request.data.get('currency')
        instance.description = request.data.get('description')
        instance.save()

        return Response(serializer.data)