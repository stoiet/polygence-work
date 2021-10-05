from rest_framework import viewsets

from spendings.serializers import SpendingsSerializer
from spendings.models import Spendings


class SpendingsViewSet(viewsets.ModelViewSet):
   queryset = Spendings.objects.all()
   serializer_class = SpendingsSerializer
