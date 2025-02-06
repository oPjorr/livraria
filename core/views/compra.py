from rest_framework.viewsets import ModelViewSet

from core.models import Compra
from core.serializers import CompraSerializer, CriarEditarCompraSerializer
from rest_framework.permissions import IsAuthenticated


class CompraViewSet(ModelViewSet):
    serializer_class = CompraSerializer
    queryset = Compra.objects.all()
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        usuario = self.request.user
        if usuario.is_superuser:
            return Compra.objects.all()
        if usuario.groups.filter(name="Administradores"):
            return Compra.objects.all()
        return Compra.objects.filter(usuario=usuario)

    def get_serializer_class(self):
        if self.action == "list":
            return CompraListSerializer
        if self.action in ("create", "update"):
            return CompraCreateUpdateSerializer
        return CompraSerializer