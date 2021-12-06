from django.db import router
from django.urls import path
from django.urls.conf import include
from demanda import views
from rest_framework.routers import DefaultRouter

app_name = 'demanda'

router = DefaultRouter()
router.register('', views.DemandaGetInsertViewSet)
router.register('finalizar', views.DemandaFinilizarViewSet, 'finalizar')

urlpatterns = [
    path('', include(router.urls)),
]