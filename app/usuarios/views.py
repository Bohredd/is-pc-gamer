# views.py
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth import login, authenticate
from .models import Usuario
from .forms import UsuarioCreationForm
from django.contrib.auth.forms import AuthenticationForm

class RegistroUsuarioView(CreateView):
    model = Usuario
    form_class = UsuarioCreationForm
    template_name = 'usuarios/registro.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        login(self.request, user)
        return super().form_valid(form)

class LoginView(FormView):
    template_name = 'usuarios/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('listar_oportunidades')  # Redirecionar após o login bem-sucedido

    def form_valid(self, form):
        email = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request=self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, 'Credenciais inválidas')
            return self.form_invalid(form)
