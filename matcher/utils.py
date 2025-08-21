import docx2txt
import pdfplumber
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

EMAIL_REGEX = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
import spacy

# Load spaCy globally
nlp = spacy.load("en_core_web_sm")

def extract_skills(text):
    doc = nlp(text.lower())
    skills = set()

    for chunk in doc.noun_chunks:
        if 2 <= len(chunk.text.strip()) <= 50:
            skills.add(chunk.text.strip())

    for token in doc:
        if token.pos_ in {"NOUN", "PROPN", "VERB"} and not token.is_stop and token.is_alpha:
            skills.add(token.lemma_.strip())

    return skills

def extract_text_from_pdf(f):
    text = []
    with pdfplumber.open(f) as pdf:
        for p in pdf.pages:
            t = p.extract_text()
            if t:
                text.append(t)
    return "\n".join(text)

def extract_text_from_docx(f):
    return docx2txt.process(f) or ""

def extract_email_from_text(text):
    m = EMAIL_REGEX.search(text)
    return m.group(0) if m else None

def calculate_score(jd_text, resume_text):
    vec = TfidfVectorizer(stop_words='english')
    mat = vec.fit_transform([jd_text, resume_text])
    return round(cosine_similarity(mat[0:1], mat[1:2])[0][0] * 100, 2)
