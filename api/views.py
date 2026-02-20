from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import InStockFilterBackend, OrderFilter, ProductFilter

from .models import Order, OrderItem, Product,User
from .serializers import (OrderSerializer, ProductInfoSerializer,
                          ProductSerializer,OrderCreateSerializer,UserSerializer)
from rest_framework.decorators import action
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

class ProductListCreateApiView(generics.ListCreateAPIView):
    queryset=Product.objects.order_by('pk')
    serializer_class=ProductSerializer  
    filterset_class=ProductFilter
    filter_backends=[DjangoFilterBackend, SearchFilter,InStockFilterBackend]
    search_fields=['name','description']

    pagination_class=PageNumberPagination
    pagination_class.page_size=2
    
    @method_decorator(cache_page(60*15,key_prefix='product_list'))

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        import time
        time.sleep(2)
        return super().get_queryset()



    

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


class OrderViewSet(viewsets.ModelViewSet):
    queryset=Order.objects.prefetch_related("items__product")
    serializer_class=OrderSerializer
    permission_classes=[IsAuthenticated]
    filterset_class=OrderFilter
    filter_backends=[DjangoFilterBackend]
    pagination_class=None

    @method_decorator(cache_page(60*15,key_prefix='order_list'))
    @method_decorator(vary_on_headers("Authorization"))

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == "create" or self.action=="update" :
            return OrderCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        qs=super().get_queryset()
        if not self.request.user.is_staff:
            qs=qs.filter(user=self.request.user)
        return qs    

    @action(detail=False,methods=['get'],url_path='user-orders',permission_classes=[IsAuthenticated])
    def user_orders(self,request):
        orders=self.get_queryset().filter(user=request.user)
        serializer=self.get_serializer(orders,many=True)
        return Response(serializer.data)
        

    



# class OrderListApiView(generics.ListAPIView):

#     queryset=Order.objects.prefetch_related("items__product")
#     serializer_class=OrderSerializer
#     filterset_class=OrderFilter
#     filter_backends=[DjangoFilterBackend,SearchFilter]

#     search_fields=['items__product__name']

# class OrderByUserApiView(generics.ListAPIView):
#     queryset=Order.objects.all()
#     serializer_class=OrderSerializer
#     permission_classes=[IsAuthenticated]
#     def get_queryset(self):
#         qs=super().get_queryset()
#         print(qs)
#         return qs.filter(user=self.request.user)




    
class ProductInfoAPiView(APIView):
    def get(self,request):
        products=Product.objects.all()
        serializer=ProductInfoSerializer({
        'products':products,
        'count':len(products),
        'max_price':products.aggregate(max_price=Max('price'))['max_price']
    })
        return Response(serializer.data)

class UserListView(generics.ListAPIView):
    queryset=User.objects.all()  
    serializer_class=UserSerializer
    pagination_class=None      



