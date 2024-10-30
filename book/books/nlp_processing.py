import spacy
from spacy.matcher import PhraseMatcher

# Cargar el modelo de spaCy
nlp = spacy.load("es_core_news_sm")  # O "en_core_web_sm" para inglés
phrase_matcher = PhraseMatcher(nlp.vocab)

# Agregar patrones para emociones, géneros, etc.
emotion_patterns = ["triste", "feliz", "enojado", "alegre", "melancólico", "desesperado"]
genre_patterns = ["misterio", "romance", "fantasía", "historia", "aventura", "drama"]
theme_patterns = ["venganza", "amor", "amistad", "superación", "traición", "justicia"]
style_patterns = ["primera", "tercera", "flashback", "epistolar", "narrativa poética"]

# Convertir los patrones a `Doc` para PhraseMatcher
emotion_patterns = [nlp.make_doc(text) for text in emotion_patterns]
genre_patterns = [nlp.make_doc(text) for text in genre_patterns]
theme_patterns = [nlp.make_doc(text) for text in theme_patterns]
style_patterns = [nlp.make_doc(text) for text in style_patterns]

# Añadir patrones al matcher
phrase_matcher.add("EMOTION", None, *emotion_patterns)
phrase_matcher.add("GENRE", None, *genre_patterns)
phrase_matcher.add("THEME", None, *theme_patterns)
phrase_matcher.add("STYLE", None, *style_patterns)


def extract_search_criteria(text):
    doc = nlp(text)

    criteria = {
        "Protagonista": [],
        "Emociones": [],
        "Lugares": [],
        "Épocas o Fechas": [],
        "Géneros": [],
        "Temas": [],
        "Estilos de Narrativa": []
    }

    # Buscar ubicaciones y fechas
    for ent in doc.ents:
        if ent.label_ == "LOC":
            criteria["Lugares"].append(ent.text)
        elif ent.label_ == "DATE":
            criteria["Épocas o Fechas"].append(ent.text)

    # Ejecutar el matcher de frases
    matches = phrase_matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        match_type = nlp.vocab.strings[match_id]

        if match_type == "EMOTION":
            criteria["Emociones"].append(span.text)
        elif match_type == "GENRE":
            criteria["Géneros"].append(span.text)
        elif match_type == "THEME":
            criteria["Temas"].append(span.text)
        elif match_type == "STYLE":
            criteria["Estilos de Narrativa"].append(span.text)

    # Extraer el protagonista y otros tokens clave
    for token in doc:
        if token.lemma_ in ["protagonista", "personaje", "héroe", "villano"]:
            criteria["Protagonista"].append(token.lemma_)

    return criteria
