from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Імʼя',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    last_name = forms.CharField(label='Прізвище',
                                widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повторення пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise ValidationError("An user with this email already exists!")
        return email


# Login form
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Імʼя',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))

    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


# Update form
class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'last_name']


class EmailChangeForm(forms.ModelForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['email']


class EmailVerificationForm(forms.Form):
    email = forms.EmailField()
