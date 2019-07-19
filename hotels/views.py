from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import UserSignupForm
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives


class SignUpView(CreateView):
    form_class = UserSignupForm
    success_url = reverse_lazy('login')
    template_name = 'auth/signup.html'


def home(request):
    return render(request,'home.html')


def send(request):

    subject = 'Subject here'
    from_mail = 'aa6653312@gmail.com'
    to_mail = ['akram.icode@gmail.com',]
    context = {
        'message': 'test message',
    }
    message = get_template('mesages/message-template.html').render(context)

    msg = EmailMultiAlternatives(subject, message, from_mail, [to_mail])
    msg.attach_alternative(message, "text/html")
    msg.send()

    return HttpResponse('done')
