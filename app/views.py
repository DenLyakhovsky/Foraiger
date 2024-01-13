import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import viewsets
from rest_framework.generics import UpdateAPIView, CreateAPIView
from rest_framework.response import Response

from rest_framework.views import APIView

from app.serializers import UserListSerializer

from app.models import Users
from app.forms import UserRegisterForm, UserLoginForm, UserUpdateForm, EmailVerificationForm, EmailChangeForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views.generic import TemplateView, DetailView, UpdateView


# Home page
class Home(TemplateView):
    template_name = 'app/home.html'


# Page about the site
class AboutSite(TemplateView):
    template_name = 'app/about.html'


# View of personal profile
@method_decorator(login_required, name='dispatch')
class UserProfileView(DetailView):
    model = User
    template_name = 'app/profile.html'
    context_object_name = 'user_profile'

    def get_object(self, queryset=None):
        return self.request.user


# Updating user data
@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'app/user_update.html'
    context_object_name = 'user_update'

    def get_object(self, queryset=None):
        return self.request.user

    # def form_valid(self, form):
    #     messages.success(self.request, 'Дані оновленні')
    #     return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['password_change_form'] = PasswordChangeForm(self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        password_change_form = PasswordChangeForm(request.user, request.POST)
        profile_change_form = UserUpdateForm(request.POST, instance=request.user)

        if password_change_form.is_valid():
            password_change_form.save()
            messages.success(request, 'Пароль успішно змінений')
            return redirect('profile')

        if profile_change_form.is_valid():
            profile_change_form.save()
            messages.success(request, 'Дані успішно змінений')
            return redirect('profile')

        else:
            messages.error(request, 'Помилка зміни паролю')
            return render(request, 'app/user_update.html',
                          {'form': self.get_form(), 'profile_change_form': profile_change_form})

    def get_success_url(self):
        return reverse_lazy('profile')


@method_decorator(login_required, name='dispatch')
class EmailChangeView(UpdateView):
    template_name = 'app/email_change.html'
    form_class = EmailChangeForm

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        self.request.user.email = form.cleaned_data['email']
        self.request.user.save()
        Users.objects.all().update(is_checked=False)
        messages.success(self.request, 'Електрона пошта успішно змінена')
        return redirect('profile')  # Замініть 'profile' на ваш URL

    def form_invalid(self, form):
        messages.error(self.request, 'Помилка зміни електронної пошти')
        return render(self.request, 'app/email_change_failed.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class EmailVerificationView(View):
    template_name = 'app/verification.html'
    success_template_name = 'app/verification_done.html'
    failure_template_name = 'app/verification_failed.html'

    def verify_email(self, email):
        api_url = f'https://api.hunter.io/v2/email-verifier?email={email}&api_key=90a3829434cd78a05b0eb08a8874a53d65557b84'

        try:
            response = requests.get(api_url)
            data = response.json()

            if response.status_code == 200 and data.get("data", {}).get("result") == "deliverable":
                return True
        except:
            pass

        return False

    def get(self, request, *args, **kwargs):
        form = EmailVerificationForm()
        user_check_email = Users.objects.all().update(is_checked=True)
        return render(request, self.template_name, {'form': form, 'user_check_email': user_check_email})

    def post(self, request, *args, **kwargs):
        form = EmailVerificationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            if self.verify_email(email):
                return render(request, self.success_template_name)
            else:
                return render(request, self.failure_template_name, {'form': form})

        return render(request, self.template_name, {'form': form})


class CreateUserAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class UserViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserListSerializer(user)
        return Response(serializer.data)


class UpdateUserView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class DetailViewUserAPI(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        person = self.get_object(pk)
        serializer = UserListSerializer(person)
        return Response(serializer.data)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form_user = form.save(commit=False)
            user_name = form.cleaned_data['username']
            email = form.cleaned_data['email']
            last_name = form.cleaned_data.get('last_name')

            form_user.username = user_name
            form_user.email = email
            form_user.last_name = last_name
            form_user.save()

            Users.objects.create(user=form_user, is_checked=False)

            login(request, form_user)
            messages.success(request, 'Successful registration')
            return redirect('home')
        else:
            messages.error(request, 'Registration error')
    else:
        form = UserRegisterForm()
    return render(request, 'app/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = UserLoginForm()
    return render(request, 'app/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')
