import django_filters
from .models import Product,Order
from rest_framework import filters



class InStockFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(stock__gt=0 )




class ProductFilter(django_filters.FilterSet):
  

    class Meta:
        model = Product
        fields ={
            'name':['exact','contains'],
            'price':['exact','lt','gt','range']
        }




class OrderFilter(django_filters.FilterSet):
    created_at=django_filters.DateFilter('created_at__date')
    class Meta:
        model=Order
        fields={
            'created_at':['lt','gt','exact'], 
            'status':['exact']
        }