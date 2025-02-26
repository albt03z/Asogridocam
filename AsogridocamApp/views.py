from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login 
from .models import News, ProductPrice
from django.conf.urls import handler404

class HomeView(TemplateView):
    """ Vista de la página de inicio """
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = News.objects.all().order_by('-extracted_at')[:5]
        return context

class SignupView(FormView):
    """ Vista de registro de usuarios """
    template_name = 'signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class LoginView(FormView):
    """ Vista de inicio de sesión """
    template_name = 'login.html'
    form_class = CustomAuthenticationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

handler404 = custom_404_view