from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import UserSignupForm
from .models import Reservation


class SignUpView(CreateView):
    form_class = UserSignupForm
    success_url = reverse_lazy('login')
    template_name = 'auth/signup.html'


# Create your views here.

def count_reservations(request):
    c_undeleted = Reservation.objects.all()
    c_deleted = Reservation.objects.deleted_only()
    c_all = Reservation.objects.all_with_deleted()
    return HttpResponse(c_deleted)

def home(request):
    return render(request,'home.html')
