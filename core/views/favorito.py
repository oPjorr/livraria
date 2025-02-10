from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from core.models import Favorito, Livro
from core.serializers import FavoritoSerializer

class FavoritoViewSet(viewsets.ModelViewSet):
    queryset = Favorito.objects.all()
    serializer_class = FavoritoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorito.objects.filter(usuario=self.request.user)

    @action(detail=True, methods=['post'])
    def favoritar(self, request, pk=None):
        livro = Livro.objects.get(pk=pk)
        favorito, created = Favorito.objects.get_or_create(usuario=request.user, livro=livro)
        if created:
            return Response({"message": "Livro favoritado com sucesso!"})
        return Response({"message": "Este livro já está nos seus favoritos."})

    @action(detail=True, methods=['post'])
    def desfavoritar(self, request, pk=None):
        livro = Livro.objects.get(pk=pk)
        favorito = Favorito.objects.filter(usuario=request.user, livro=livro)
        if favorito.exists():
            favorito.delete()
            return Response({"message": "Livro removido dos favoritos!"})
        return Response({"message": "Este livro não está nos seus favoritos."})
