
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView
from accounts.views import SignUpView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='auth/login.html',success_url='hotels:home'), name="login"),
    path('signup/', SignUpView.as_view(), name='signup'), # new
    path('', include('django.contrib.auth.urls')), # new
    path('', include('hotels.urls')),
]
