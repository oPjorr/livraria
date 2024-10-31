from rest_framework import viewsets
from core.models import Livro
from core.serializers import LivroDetailSerializer, LivroSerializer

class LivroViewSet(viewsets.ModelViewSet):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return LivroDetailSerializer
        return LivroSerializer