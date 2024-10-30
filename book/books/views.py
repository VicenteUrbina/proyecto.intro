from django.shortcuts import render
from django.db.models import Q
from .models import Book
from .forms import SearchForm
from .nlp_processing import extract_search_criteria

def search_books(request):
    form = SearchForm()
    results = []  # Inicia vacío para no mostrar nada por defecto
    matched_criteria = {}  # Inicializa matched_criteria vacío para todas las solicitudes

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            criteria = extract_search_criteria(query)

            filters = Q()
            match_count = {}  # Para almacenar el recuento de coincidencias

            # Filtrado inicial con criterios usando OR en cada categoría
            if criteria["Protagonista"]:
                for protagonist in criteria["Protagonista"]:
                    filters |= Q(summary__icontains=protagonist) | Q(tags__icontains=protagonist)

            if criteria["Emociones"]:
                for emotion in criteria["Emociones"]:
                    filters |= Q(tags__icontains=emotion) | Q(summary__icontains=emotion)

            if criteria["Lugares"]:
                for location in criteria["Lugares"]:
                    filters |= Q(tags__icontains=location) | Q(summary__icontains=location)

            if criteria["Épocas o Fechas"]:
                for time in criteria["Épocas o Fechas"]:
                    filters |= Q(tags__icontains=time) | Q(summary__icontains=time)

            if criteria["Géneros"]:
                for genre in criteria["Géneros"]:
                    filters |= Q(tags__icontains=genre) | Q(summary__icontains=genre)

            if criteria["Temas"]:
                for theme in criteria["Temas"]:
                    filters |= Q(tags__icontains=theme) | Q(summary__icontains=theme)

            if criteria["Estilos de Narrativa"]:
                for style in criteria["Estilos de Narrativa"]:
                    filters |= Q(tags__icontains=style) | Q(summary__icontains=style)

            # Aplicar filtros y ponderar los resultados según la cantidad de coincidencias
            results = Book.objects.filter(filters).distinct()
            for book in results:
                count = 0

                # Contar coincidencias y registrar criterios en matched_criteria
                matched_tags = []  # Lista para almacenar los criterios que cumple el libro

                if criteria["Protagonista"]:
                    if any(protagonist in book.summary or protagonist in book.tags for protagonist in
                           criteria["Protagonista"]):
                        count += 1
                        matched_tags.append("Protagonista")

                if criteria["Emociones"]:
                    if any(emotion in book.summary or emotion in book.tags for emotion in criteria["Emociones"]):
                        count += 1
                        matched_tags.append("Emociones")

                if criteria["Lugares"]:
                    if any(location in book.summary or location in book.tags for location in criteria["Lugares"]):
                        count += 1
                        matched_tags.append("Lugares")

                if criteria["Épocas o Fechas"]:
                    if any(time in book.summary or time in book.tags for time in criteria["Épocas o Fechas"]):
                        count += 1
                        matched_tags.append("Épocas o Fechas")

                if criteria["Géneros"]:
                    if any(genre in book.summary or genre in book.tags for genre in criteria["Géneros"]):
                        count += 1
                        matched_tags.append("Géneros")

                if criteria["Temas"]:
                    if any(theme in book.summary or theme in book.tags for theme in criteria["Temas"]):
                        count += 1
                        matched_tags.append("Temas")

                if criteria["Estilos de Narrativa"]:
                    if any(style in book.summary or style in book.tags for style in criteria["Estilos de Narrativa"]):
                        count += 1
                        matched_tags.append("Estilos de Narrativa")

                match_count[book] = count
                matched_criteria[book] = matched_tags  # Asigna los criterios coincidentes al libro en matched_criteria

            # Ordenar según el recuento de coincidencias
            sorted_books = sorted(match_count.items(), key=lambda x: x[1], reverse=True)
            results = [book[0] for book in sorted_books]  # Obtener solo los libros

            # Búsqueda general si no hay resultados específicos
            if not results:
                results = Book.objects.filter(
                    Q(title__icontains=query) |
                    Q(tags__icontains=query) |
                    Q(summary__icontains=query)
                )

    return render(request, 'search.html', {'form': form, 'results': results, 'matched_criteria': matched_criteria})



def home(request):
    return render(request, 'home.html')  # Crea una plantilla llamada home.html
