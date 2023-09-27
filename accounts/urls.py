from django.urls import path, include
from rest_framework import routers
from . import views

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='login'),
    path('refresh_token/', TokenRefreshView.as_view(), name='refresh_token'),
    path('cantones/<int:provincia_id>/', views.cantones, name='cantones'),
    path('provincias/', views.provincias, name='provincias'),
    path('eventos/', views.eventos, name='eventos'),
    path('resultados_votos/', views.resultados_votos, name='resultados_votos'),
    path('confirmation/<str:pk>/<str:uid>/', views.confirmation, name='email_confirmation'),
    path("", include(router.urls)),
]
