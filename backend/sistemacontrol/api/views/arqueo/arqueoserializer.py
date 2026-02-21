from rest_framework import serializers
from dashboard.models import Arqueo


class ArqueoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arqueo
        fields = "__all__"
