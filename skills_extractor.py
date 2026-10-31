import spacy
from spacy.matcher import PhraseMatcher

# Load spaCy pipeline; disable parser and ner to maximize extraction speed
nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

# 1. Define Standard Tech Stack and Certifications
DEFAULT_TECH_SKILLS = [
    # Languages & Frameworks
    "Python", "SQL", "MySQL", "PostgreSQL", "MongoDB", "Cassandra", "C++", "Java", "JavaScript",
    "FastAPI", "Flask", "Django", "React", "Node.js", "HTML", "CSS",
    # Data Science, ML & Big Data
    "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "Keras", "PyTorch", "PySpark", 
    "Apache Airflow", "Apache Spark", "Hadoop", "Power BI", "Tableau", "Excel",
    # Cloud, DevOps & Tools
    "Git", "GitHub", "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Linux", "CI/CD", "Redis"
]

DEFAULT_CERTIFICATIONS = [
    "AWS Certified Solutions Architect", "AWS Certified Cloud Practitioner",
    "Microsoft Certified: Azure Fundamentals", "Azure Solutions Architect",
    "Google Cloud Certified", "PMP", "Certified Kubernetes Administrator",
    "CKA", "CISSP", "CompTIA Security+", "TensorFlow Developer Certificate"
]

def build_matcher():
    """Initializes PhraseMatcher with case-insensitive token matching."""
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    
    skill_patterns = [nlp.make_doc(text) for text in DEFAULT_TECH_SKILLS]
    cert_patterns = [nlp.make_doc(text) for text in DEFAULT_CERTIFICATIONS]
    
    matcher.add("TECH_SKILL", skill_patterns)
    matcher.add("CERTIFICATION", cert_patterns)
    return matcher

matcher = build_matcher()

def extract_entities(text: str):
    """
    Parses input text and extracts unique technical skills and certifications.
    """
    doc = nlp(text)
    matches = matcher(doc)
    
    extracted_skills = set()
    extracted_certs = set()
    
    for match_id, start, end in matches:
        label = nlp.vocab.strings[match_id]
        span_text = doc[start:end].text.strip()
        
        # Match case canonicalization
        if label == "TECH_SKILL":
            extracted_skills.add(span_text.title())
        elif label == "CERTIFICATION":
            extracted_certs.add(span_text)
            
    return {
        "skills": sorted(list(extracted_skills)),
        "certifications": sorted(list(extracted_certs))
    }

if __name__ == "__main__":
    sample = "Experienced in Python, PySpark, and FastAPI with AWS Certified Solutions Architect credential."
    print(extract_entities(sample))
