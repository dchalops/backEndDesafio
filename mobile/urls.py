from django.urls import path
from .authentication import LoginView
from .index import IndexView

urlpatterns = [
    path('v1/auth/', LoginView.as_view(), name='login'),
    path('v1/home/', IndexView.as_view(), name='index_view'),
]
