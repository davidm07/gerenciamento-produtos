from . import views
from django.urls import path

urlpatterns = [
    path('produtos/', views.getProdutos),
    path('produtos/cadastrar', views.postProdutos),
    path('produtos/<id>', views.getProdutosId),
    
]