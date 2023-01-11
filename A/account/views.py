from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.


class RegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'account/register.html'

    # dispatch ghabl baghiye ejra mishe masalan inja check mikone ke karbar az tarigh url natone vared she
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(cd['username'], cd['email'], cd['password'])
            user.first_name = cd['first_name']
            user.last_name = cd['last_name']
            messages.success(request, 'Todo registered successfully', 'success')
            return redirect('home:home')
        return render(request, self.template_name, {'form': form})


class LoginView(View):
    form_class = UserLoginForm
    template_name = 'account/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'Todo login successfully', 'success')
                return redirect('home:home')
            messages.error(request, 'Error', 'warning')
        return render(request, self.template_name, {'form': form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Todo logout successfully', 'success')
        return redirect('home:home')


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        return render(request, 'account/profile.html', {'user': user})
