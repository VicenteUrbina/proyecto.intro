from django.urls import path
from . import views  # Importa las vistas desde el archivo views.py

urlpatterns = [
    path('search/', views.search_books, name='search_books'),
]
