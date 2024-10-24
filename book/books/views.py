from django.shortcuts import render
from .models import Book
from .forms import SearchForm


def search_books(request):
    form = SearchForm()
    results = []

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Book.objects.filter(
                title__icontains=query) | Book.objects.filter(
                tags__icontains=query) | Book.objects.filter(
                summary__icontains=query)

    return render(request, 'search.html', {'form': form, 'results': results})
def home(request):
    return render(request, 'home.html')  # Crea una plantilla llamada home.html