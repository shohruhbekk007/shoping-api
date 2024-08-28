from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    XaridorViewSet, MahsulotViewSet, PartiyaViewSet, SkladViewSet, SotuvViewSet,RegisterAPIView, LoginAPIView, LogoutAPIView,
    tushum_statistika, eng_kop_sotilgan_tovar, umumiy_sotuv_tovarlar_kesimida,
    yoqotishlar_qarzdorlar, umumiy_tovarlar,
)
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Ombor Boshqaruv Tizimi API",
        default_version='v1',
        description="Ombor boshqaruv tizimi uchun API hujjatlari",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@ombor.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


router = DefaultRouter()
router.register(r'xaridorlar', XaridorViewSet)
router.register(r'mahsulotlar', MahsulotViewSet)
router.register(r'partiya', PartiyaViewSet)
router.register(r'sklad', SkladViewSet)
router.register(r'sotuvlar', SotuvViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/statistika/tushum/', tushum_statistika),
    path('api/statistika/eng_kop_sotilgan_tovar/', eng_kop_sotilgan_tovar),
    path('api/statistika/umumiy_sotuv_tovarlar_kesimida/', umumiy_sotuv_tovarlar_kesimida),
    path('api/statistika/yoqotishlar_qarzdorlar/', yoqotishlar_qarzdorlar),
    path('api/statistika/umumiy_tovarlar/', umumiy_tovarlar),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/register/', RegisterAPIView.as_view(), name='register'),
    path('api/login/', LoginAPIView.as_view(), name='login'),
    path('api/logout/', LogoutAPIView.as_view(), name='logout'),
]
