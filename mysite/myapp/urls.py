from django.urls import path
from . import views
urlpatterns =[
    path('', views.home, name='myapp'),
    path('myapp/', views.signup, name='myapp')
]