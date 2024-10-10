from django.db import models

# Create your models here.
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    quantidade_em_estoque = models.IntegerField()
    data_criacao = models.DateTimeField

    def __str__(self):
        return self.nome