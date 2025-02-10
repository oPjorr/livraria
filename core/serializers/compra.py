from rest_framework.serializers import (
    CharField,
    CurrentUserDefault,
    DateTimeField,
    HiddenField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
)

from core.models import Compra, ItensCompra


class ItensCompraSerializer(ModelSerializer):
    total = SerializerMethodField()

    def get_total(self, instance):
        return instance.livro.preco * instance.quantidade

    class Meta:
        model = ItensCompra
        fields = ("livro", "quantidade", "total")
        depth = 1


class CriarEditarItensCompraSerializer(ModelSerializer):
    class Meta:
        model = ItensCompra
        fields = ("livro", "quantidade")

    def validate(self, data):
        if data["quantidade"] > data["livro"].quantidade:
            raise ValidationError({"quantidade": "Quantidade solicitada não disponível em estoque."})
        return data


class CompraSerializer(ModelSerializer):
    usuario = CharField(source="usuario.email", read_only=True)
    status = CharField(source="get_status_display", read_only=True)
    data = DateTimeField(read_only=True)
    tipo_pagamento = CharField(source="get_tipo_pagamento_display", read_only=True)
    itens = ItensCompraSerializer(many=True, read_only=True)

    class Meta:
        model = Compra
        fields = ("id", "usuario", "status", "total", "data", "tipo_pagamento", "itens")


class CriarEditarCompraSerializer(ModelSerializer):
    usuario = HiddenField(default=CurrentUserDefault())
    itens = CriarEditarItensCompraSerializer(many=True)

    class Meta:
        model = Compra
        fields = ("usuario", "itens")

    def create(self, validated_data):
        itens = validated_data.pop("itens")
        usuario = validated_data["usuario"]

        compra, criada = Compra.objects.get_or_create(
            usuario=usuario, status=Compra.StatusCompra.CARRINHO, defaults=validated_data
        )

        for item in itens:
            item_existente = compra.itens.filter(livro=item["livro"]).first()

            if item_existente:
                item_existente.quantidade += item["quantidade"]
                item_existente.preco = item["livro"].preco
                item_existente.save()
            else:
                item["preco"] = item["livro"].preco
                ItensCompra.objects.create(compra=compra, **item)

        compra.save()
        return compra

    def update(self, compra, validated_data):
        itens = validated_data.pop("itens", [])
        if itens:
            compra.itens.all().delete()
            for item in itens:
                item["preco"] = item["livro"].preco
                ItensCompra.objects.create(compra=compra, **item)

        return super().update(compra, validated_data)