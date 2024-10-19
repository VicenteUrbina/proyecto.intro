from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
def home(request):
    return render(request,'home.html')
def singup(request):
    return render(request,'index.html')