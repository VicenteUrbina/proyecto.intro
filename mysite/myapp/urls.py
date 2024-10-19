from django.urls import path
from . import views
urlpatterns =[
    path('', views.home, name='myapp'),
    path('myapp/', views.singup, name='myapp')
]