from rest_framework import serializers
from core.models import Favorito

class FavoritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorito
        fields = ["id", "usuario", "livro", "data_adicionado"]
