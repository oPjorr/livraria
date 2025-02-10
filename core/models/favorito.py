from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Favorito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favoritos")
    livro = models.ForeignKey("Livro", on_delete=models.CASCADE, related_name="favoritado_por")
    data_adicionado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("usuario", "livro")

    def __str__(self):
        return f"{self.usuario} favoritou {self.livro}"