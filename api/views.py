from django.shortcuts import render
from .models import Product,Order,OrderItem
from .serializers import ProductSerializer,OrderSerializer,ProductInfoSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Max
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.permissions import (
    IsAuthenticated,IsAdminUser,AllowAny
)
from rest_framework.views import APIView



class ProductListCreateApiView(generics.ListCreateAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    def get_permissions(self):
        self.permission_classes=[AllowAny]
        if self.request.method=="POST":
            self.permission_classes=[IsAdminUser]
        return super().get_permissions()

    



class ProductDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    def get_permissions(self):
        self.permission_classes=[AllowAny]
        if self.request.method in ["PUT","PATCH","DELETE"]:
            self.permission_classes=[IsAdminUser]
        return super().get_permissions()


class OrderListApiView(generics.ListAPIView):
    queryset=Order.objects.prefetch_related("items__product")
    serializer_class=OrderSerializer

class OrderByUserApiView(generics.ListAPIView):
    queryset=Order.objects.all()
    serializer_class=OrderSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        qs=super().get_queryset()
        print(qs)
        return qs.filter(user=self.request.user)




    
class ProductInfoAPiView(APIView):
    def get(self,request):
        products=Product.objects.all()
        serializer=ProductInfoSerializer({
        'products':products,
        'count':len(products),
        'max_price':products.aggregate(max_price=Max('price'))['max_price']
    })
        return Response(serializer.data)
        



