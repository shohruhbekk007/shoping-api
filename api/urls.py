from django.urls import path, include
from . import views
from .views import StatistikaViewSet, SotuvViewSet, partiya_list, partiya_detail, partiya_create, partiya_delete, partiya_update
from rest_framework.routers import DefaultRouter
from .views import SotuvViewSet

# Router yaratamiz
router = DefaultRouter()
router.register(r'sotuv', SotuvViewSet, basename='sotuv')
router.register(r'statistika', StatistikaViewSet, basename='statistika')



urlpatterns = [
    path('xaridorlar/', views.xaridor_list, name='xaridor_list'),
    path('xaridorlar/<int:pk>/', views.xaridor_detail, name='xaridor_detail'),
    path('xaridorlar/<int:pk>/qarz_sondirish/', views.qarz_sondirish, name='qarz_sondirish'),
    path('qarzdorlar/', views.qarzdorlar_korsatish, name='qarzdorlar_korsatish'),
    path('maxsulotlar/', views.maxsulotlar_list, name='maxsulotlar_list'),
    path('maxsulotlar/<int:pk>/', views.maxsulotlar_detail, name='maxsulotlar_detail'),
    path('partiya/', partiya_list, name='partiya-list'),
    path('partiya/create/', partiya_create, name='partiya-create'),
    path('partiya/<int:pk>/', partiya_detail, name='partiya-detail'),
    path('partiya/<int:pk>/update/', partiya_update, name='partiya-update'),
    path('partiya/<int:pk>/delete/', partiya_delete, name='partiya-delete'),
    path('', include(router.urls)),
]
