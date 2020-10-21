from rest_framework import serializers
from .models import TheCar

class TheCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheCar
        fields = ('make', 'model', 'rate1', 'rate2', 'rate3', 'rate4', 'rate5', 'rates')



