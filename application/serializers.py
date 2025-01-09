from rest_framework import serializers
from .models import sumanmodel

class sumanserializers(serializers.ModelSerializer):
    

    class Meta:
        model=sumanmodel
        fields='__all__'
        