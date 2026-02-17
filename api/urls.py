from django.urls import path,include
from . import views
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path("products/",views.ProductListCreateApiView.as_view()),
   
      path("products/info/",views.ProductInfoAPiView.as_view()),
    path("products/<int:pk>/",views.ProductDetailApiView.as_view()),
    path("orders/",views.OrderListApiView.as_view()),
   
    path('user-order/',views.OrderByUserApiView.as_view(),name="user_orders"),
     # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    ]
