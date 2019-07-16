from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import UserSignupForm


class SignUpView(CreateView):
    form_class = UserSignupForm
    success_url = reverse_lazy('login')
    template_name = 'auth/signup.html'
