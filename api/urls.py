from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import (
    RevenueAPIView, 
    TopSellingProductsAPIView, 
    LeastSellingProductsAPIView, 
    TotalSalesByProductAPIView,
    LossesAPIView, 
    DebtorsAPIView,
    ProductStockAPIView,
    ProductsViewSet, WarehouseViewSet, PartysViewSet, BuyersViewSet
)
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

router = DefaultRouter()
router.register(r'products', ProductsViewSet)
router.register(r'warehouse', WarehouseViewSet)
router.register(r'partys', PartysViewSet)
router.register(r'buyers', BuyersViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="API Dokumentatsiya",
        default_version='v1',
        description="Bu API uchun hujjatlashtirish",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@myapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', include(router.urls)),
    path('revenue/', RevenueAPIView.as_view(), name='revenue'),
    path('top-selling/', TopSellingProductsAPIView.as_view(), name='top-selling'),
    path('least-selling/', LeastSellingProductsAPIView.as_view(), name='least-selling'),
    path('total-sales/', TotalSalesByProductAPIView.as_view(), name='total-sales'),
    path('losses/', LossesAPIView.as_view(), name='losses'),
    path('debtors/', DebtorsAPIView.as_view(), name='debtors'),
    path('stock/', ProductStockAPIView.as_view(), name='stock'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),
]
