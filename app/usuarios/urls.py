# urls.py
from django.urls import path
from .views import RegistroUsuarioView, LoginView

urlpatterns = [
    path('registro/', RegistroUsuarioView.as_view(), name='registro_usuario'),
    path('login/', LoginView.as_view(), name='login'),
    # Outras URLs...
]
