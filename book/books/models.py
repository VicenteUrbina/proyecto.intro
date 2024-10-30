from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    summary = models.TextField()  # Resumen del libro
    tags = models.CharField(max_length=200)  # Etiquetas clave separadas por comas
    genre = models.CharField(max_length=100, blank=True)  # Género del libro
    period = models.CharField(max_length=100, blank=True)  # Época
    location = models.CharField(max_length=100, blank=True)  # Lugar de la historia
    protagonist_mood = models.CharField(max_length=100, blank=True)  # Estado emocional del protagonista
    theme = models.CharField(max_length=200, blank=True)  # Tema de la historia
    secondary_characters = models.CharField(max_length=200, blank=True)  # Características de personajes secundarios
    setting = models.CharField(max_length=200, blank=True)  # Descripción del ambiente

    def __str__(self):
        return self.title


