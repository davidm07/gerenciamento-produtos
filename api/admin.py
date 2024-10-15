from django.contrib import admin
from .models import Produto
from api import models

# Register your models here.
@admin.register(models.Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'preco')
    list_display_links = ('nome',)
    list_filter = ('categoria', 'preco')
    search_fields= ('nome',)
    list_editable = ('preco',)