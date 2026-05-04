
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.http import  HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from user.forms import LoginUserForm, RegisterUserForm


class UserRegisterView(CreateView):
    model = get_user_model()
    form_class = RegisterUserForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('user:login')


class UserLoginView(LoginView):
    form_class = LoginUserForm
    template_name = 'user/login.html'


class UserProfileView(DetailView):
    model = get_user_model()
    template_name = 'user/profile.html'
    pk_url_kwarg = "user_id"
    context_object_name = 'user'

def check_username(request):
    username = request.GET.get('username', '')
    if len(username) > 3:
        if get_user_model().objects.filter(username=username).exists():
            return HttpResponse("<span style='color: red; font-weight: 800;font-size: 11px;'>Username is not available</span>")
        else:
            return HttpResponse("<span style='color: green; font-weight: 800;font-size: 11px;'>Username is available</span>")
    return HttpResponse('')

def check_email(request):
    email = request.GET.get('email', '')
    if len(email) > 5:
        if get_user_model().objects.filter(email=email).exists():
            return HttpResponse("<span style='color: red; font-weight: 800; font-size: 11px;'>Email is not available</span>")
        else:
            return HttpResponse("<span style='color: green; font-weight: 800; font-size: 11px;'>Email is available</span>")
    return HttpResponse('')
