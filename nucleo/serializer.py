from rest_framework import serializers
from nucleo.models import Participate, Proyect  

class ParticipateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participate
        fields = ['clientId', 'proyectId', 'role']
        
class ProyectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyect
        fields = '__all__'