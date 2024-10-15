from typing import List
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .models import Produto
from . import serializers
from drf_yasg.utils import swagger_auto_schema
from rest_framework.pagination import PageNumberPagination
from drf_yasg import openapi
from django.db.models import Q

# Create your views here.

@swagger_auto_schema(
    methods=["GET"],
    manual_parameters=[
        openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
        openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
        openapi.Parameter('nome', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter('categoria', openapi.IN_QUERY, type=openapi.TYPE_STRING),
    ],
    tags=['Produtos'],
)
@api_view(['GET'])
def getProdutos(request):
    paginator = PageNumberPagination()
    paginator.page_size = request.query_params.get('page_size', 5)

    # Obtém os filtros dos parâmetros da consulta
    name_filter = request.query_params.get('nome', None)
    category_filter = request.query_params.get('categoria', None)

    # Monta a consulta
    produtos = Produto.objects.all()
    conditions = Q()

    if name_filter:
        conditions |= Q(nome__icontains=name_filter)

    if category_filter:
        conditions |= Q(categoria__icontains=category_filter)

    produtos = produtos.filter(conditions)

    paginated_produtos = paginator.paginate_queryset(produtos, request)
    serializer = serializers.ProdutoSerializer(paginated_produtos, many=True)
    return paginator.get_paginated_response(serializer.data)

@swagger_auto_schema(
    methods=["POST"],
    tags=['Produtos'],
    request_body= serializers.ProdutoSerializer(many=True),
)
@api_view(['POST'])
def postProdutos(request):
    serializer = serializers.ProdutoSerializer(data=request.data, many=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    methods=["GET", "DELETE"],
    tags=['Produtos'],
)
@swagger_auto_schema(
    methods=['PUT'],
    request_body=serializers.ProdutoSerializer,
    tags=['Produtos'],
)
@api_view(['GET', 'PUT', 'DELETE'])
def getProdutosId(request, id):
    produto = Produto.objects.get(id=id)
    if request.method == 'GET':
        serializer = serializers.ProdutoSerializer(produto)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = serializers.ProdutoSerializer(produto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        produto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
 