from rest_framework import serializers
from dashboard.models import Categoria


class CategoriasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = "__all__"
        read_only_fields = ["empresa"]
