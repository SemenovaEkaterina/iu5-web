from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.models import User
from .models import Profile, Tag, Question, Answer


class LoginForm(forms.Form):
    login = forms.CharField(label='Login')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class SettingsForm(forms.Form):
    login = forms.CharField(label='Login', min_length=5, required=False)
    email = forms.CharField(label='Email', required=False)
    password = forms.CharField(label='Password', min_length=6, widget=forms.PasswordInput)
    repeat_password = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    avatar = forms.ImageField(label='Upload avatar', required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(SettingsForm, self).__init__(*args, **kwargs)

    def clean_login(self):
        login = self.cleaned_data['login']
        if self.user.name != login:
            if User.objects.filter(username=login):
                raise ValidationError('this login is already used')
        return login

    def clean_email(self):
        validate_email(self.cleaned_data['email'])
        return self.cleaned_data['email']

    def clean(self):
        cleaned_data = super(SettingsForm, self).clean()
        if self.cleaned_data.get('password') and self.cleaned_data.get('repeat_password'):
            if self.cleaned_data['password'] != self.cleaned_data['repeat_password']:
                raise ValidationError('passwords are not equal')
        return cleaned_data

    def save(self):
        user = User.objects.get(username=self.user.name)
        if self.cleaned_data['login']:
            user.username = self.cleaned_data['login']
        if self.cleaned_data['email']:
            user.email = self.cleaned_data['email']
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])
        user.save()
        profile = Profile.objects.get(user=user)
        if self.cleaned_data['avatar']:
            profile.avatar = self.cleaned_data['avatar']
        profile.save()
        return profile


class SignupForm(forms.Form):
    login = forms.CharField(label='Login', min_length=5)
    email = forms.CharField(label='Email')
    password = forms.CharField(label='Password', min_length=6, widget=forms.PasswordInput)
    repeat_password = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    avatar = forms.ImageField(label='Upload avatar', required=False)

    def clean_login(self):
        login = self.cleaned_data['login']
        if User.objects.filter(username=login):
            raise ValidationError('this login is already used')
        return login

    def clean_email(self):
        validate_email(self.cleaned_data['email'])
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
                                        password=self.cleaned_data['password'])
        if self.cleaned_data['avatar'] is None:
            profile = Profile.objects.create(user=user)
        else:
            profile = Profile.objects.create(user=user, avatar=self.cleaned_data['avatar'])
        return profile


class AskForm(forms.Form):

    title = forms.CharField(label='Title')
    text = forms.CharField(label='Text', widget=forms.Textarea(attrs={'rows': 7}))
    tags = forms.CharField(label='Tags')

    def save(self, user):
        profile = Profile.objects.get(user=user)
        question = Question(author=profile,
                            title=self.cleaned_data['title'],
                            text=self.cleaned_data['text'])
        question.save()
        tags = self.cleaned_data['tags'].split(' ')
        for i in tags:
            tag = Tag.objects.get_or_create(name=i)[0]
            question.tags.add(tag)
        question.save()
        return question


class AnswerForm(forms.Form):
    text = forms.CharField(label='Text', widget=forms.Textarea(attrs={'rows': 4, 'cols': 86}))

    def save(self, user, question):
        profile = Profile.objects.get(user=user)
        answer = Answer.objects.create(text=self.cleaned_data['text'],
                                       author=profile,
                                       question=question)
        return answer
