from django.shortcuts import render
from django.views import View
from .forms import UserRegistrationForm
# Create your views here.


class RegisterView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'account/register.html', {'form': form})

    def post(self, request):
        return render(request, 'account/register.html')