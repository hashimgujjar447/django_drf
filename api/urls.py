from django.urls import path,include
from . import views
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path("products/",views.ProductListCreateApiView.as_view()),
   
      path("products/info/",views.ProductInfoAPiView.as_view()),
    path("products/<int:pk>/",views.ProductDetailApiView.as_view()),
   
     # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    ]


router=DefaultRouter()
router.register('orders',views.OrderViewSet)

urlpatterns+=router.urls