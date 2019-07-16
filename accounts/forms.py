from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

class UserSignupForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = get_user_model()
        fields = ('username', 'email')


class UserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = get_user_model()
        fields = UserChangeForm.Meta.fields


class UserForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email')
        # fields = "__all__"
