import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from skills_extractor import extract_entities

ACTION_VERBS = {
    "led", "developed", "managed", "created", "designed", "implemented", 
    "optimized", "engineered", "built", "spearheaded", "reduced", "increased", 
    "delivered", "analyzed", "automated", "streamlined", "orchestrated"
}

STANDARD_SECTIONS = [
    "experience", "work history", "education", "skills", 
    "projects", "certifications", "summary", "objective"
]

def analyze_without_jd(resume_text):
    text_lower = resume_text.lower()
    feedback = []
    score = 100

    # 1. Core Section Detection
    detected = [s for s in STANDARD_SECTIONS if s in text_lower]
    missing = [s for s in ["experience", "education", "skills"] if s not in detected]
    if missing:
        score -= len(missing) * 10
        feedback.append(f"Missing core sections: {', '.join(missing).title()}.")

    # 2. Contact Information Check
    has_email = bool(re.search(r'[\w\.-]+@[\w\.-]+\.\w+', resume_text))
    has_phone = bool(re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', resume_text))
    has_profile = bool(re.search(r'linkedin\.com|github\.com', text_lower))

    if not has_email:
        score -= 10
        feedback.append("Missing or unreadable email address.")
    if not has_phone:
        score -= 10
        feedback.append("Missing or invalid phone number formatting.")
    if not has_profile:
        score -= 5
        feedback.append("Consider adding a LinkedIn or GitHub profile link.")

    # 3. Action Verb & Impact Metric Count
    words = re.findall(r'\b\w+\b', text_lower)
    action_verb_count = sum(1 for w in words if w in ACTION_VERBS)
    metrics_count = len(re.findall(r'(\d+%\b|\$\d+|\b\d+\+?\b)', resume_text))

    if action_verb_count < 5:
        score -= 10
        feedback.append("Low strong action verb count. Use verbs like 'Engineered', 'Optimized', or 'Managed'.")
    if metrics_count < 3:
        score -= 10
        feedback.append("Few quantifiable metrics detected (KPIs, %, revenue figures).")

    # 4. Resume Length & Volume
    word_count = len(words)
    if word_count < 250:
        score -= 15
        feedback.append("Resume is too brief (under 250 words). Provide deeper scope on duties.")
    elif word_count > 1200:
        score -= 10
        feedback.append("Resume exceeds 1200 words. Condense to keep it ATS-friendly.")

    return {
        "score": max(0, min(score, 100)),
        "word_count": word_count,
        "action_verb_count": action_verb_count,
        "feedback": feedback if feedback else ["Formatting and structure adhere to ATS standards."]
    }

def analyze_with_jd(resume_text, jd_text):
    hygiene = analyze_without_jd(resume_text)

    # TF-IDF N-Gram Vectorization for Semantic Alignment
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
    
    # Cosine Similarity between resume and job description
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    match_pct = round(similarity * 100, 2)

    # Extract high-weight keywords from JD
    feature_names = vectorizer.get_feature_names_out()
    jd_scores = tfidf_matrix[1].toarray()[0]
    top_indices = jd_scores.argsort()[::-1][:30]
    
    resume_lower = resume_text.lower()
    missing_keywords = [
        feature_names[i] for i in top_indices 
        if jd_scores[i] > 0.05 and feature_names[i] not in resume_lower
    ]

    # Weighted aggregate score: 60% Keyword Relevance + 40% Resume Hygiene
    overall_score = round((match_pct * 0.6) + (hygiene["score"] * 0.4), 2)
    feedback = hygiene["feedback"].copy()

    if match_pct < 35:
        feedback.append("Low keyword coverage against this job description. Incorporate required core competencies.")

    spacy_res = analyze_with_jd_spacy(resume_text, jd_text)

    return {
        "overall_fit_score": overall_score,
        "match_percentage": match_pct,
        "hygiene_score": hygiene["score"],
        "word_count": hygiene["word_count"],
        "action_verb_count": hygiene["action_verb_count"],
        "missing_keywords": missing_keywords[:15],
        "feedback": feedback,
        **spacy_res
    }

def analyze_with_jd_spacy(resume_text, jd_text):
    # 1. Run extraction on both texts
    resume_data = extract_entities(resume_text)
    jd_data = extract_entities(jd_text)
    
    resume_skills = set(k.lower() for k in resume_data["skills"])
    jd_skills = set(k.lower() for k in jd_data["skills"])
    
    resume_certs = set(k.lower() for k in resume_data["certifications"])
    jd_certs = set(k.lower() for k in jd_data["certifications"])
    
    # 2. Identify Matches and Gaps
    matched_skills = [s.title() for s in jd_skills if s in resume_skills]
    missing_skills = [s.title() for s in jd_skills if s not in resume_skills]
    
    matched_certs = [c for c in jd_certs if c in resume_certs]
    missing_certs = [c for c in jd_certs if c not in resume_certs]
    
    # 3. Calculate Direct Skills Match Percentage
    total_required = len(jd_skills) + len(jd_certs)
    if total_required > 0:
        matched_count = len(matched_skills) + len(matched_certs)
        skill_score = round((matched_count / total_required) * 100, 2)
    else:
        skill_score = 100.0  # No explicit technical criteria listed in JD

    return {
        "skill_score": skill_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "matched_certifications": matched_certs,
        "missing_certifications": missing_certs,
        "all_resume_skills": resume_data["skills"],
        "all_resume_certifications": resume_data["certifications"]
    }

