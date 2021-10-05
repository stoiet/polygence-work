from rest_framework import viewsets

from spendings.serializers import SpendingsSerializer
from spendings.models import Spendings


class SpendingsViewSet(viewsets.ModelViewSet):
   queryset = Spendings.objects.all()
   serializer_class = SpendingsSerializer

   def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
