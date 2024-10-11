from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
def myapp(request):
    return render(request,'index.html',{
        'form': UserCreationForm
    })