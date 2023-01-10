from django.shortcuts import render
from django.http import HttpResponse
from django.views import View


# Create your views here.


class HomeView(View):
    def get(self, request):
        return render(request, 'home/index.html')

    def post(self, request):
        return render(request, 'home/index.html')
