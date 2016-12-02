from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    login = forms.CharField(label='Login')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class SignupForm(forms.Form):
    login = forms.CharField(label='Login', min_length=5)
    email = forms.CharField(label='Email')
    first_name = forms.CharField(label='First name')
    last_name = forms.CharField(label='Last name')
    password = forms.CharField(label='Password', min_length=8, widget=forms.PasswordInput)
    repeat_password = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    def clean_login(self):
        login = self.cleaned_data['login']
        if User.objects.filter(username=login):
            raise ValidationError('this login is already used')
        return login

    def clean_email(self):
        validate_email( self.cleaned_data['email'])
        return self.cleaned_data['email']

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        if self.cleaned_data.get('password') and self.cleaned_data.get('repeat_password'):
            if self.cleaned_data['password'] != self.cleaned_data['repeat_password']:
                raise ValidationError('passwords are not equal')
        return cleaned_data

    def save(self):
        user = User.objects.create_user(username=self.cleaned_data['login'],
                                        email=self.cleaned_data['email'],
                                        password=self.cleaned_data['password'],
                                        first_name=self.cleaned_data['first_name'],
                                        last_name=self.cleaned_data['last_name'],
                                        )
        return user