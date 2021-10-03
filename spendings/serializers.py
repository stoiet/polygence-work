from rest_framework import serializers

from spendings.models import Spendings

class SpendingsSerializer(serializers.ModelSerializer):
   class Meta:
       model = Spendings
       fields = ('amount', 'currency', 'description')
