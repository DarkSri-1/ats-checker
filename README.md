# ApexATS — Next-Gen Resume & JD Intelligence

ApexATS is an intelligent Applicant Tracking System (ATS) resume evaluator and parser built with Python, Flask, spaCy, and scikit-learn. It features a modern dark-slate glassmorphism dashboard, multi-stage document ingestion, exact skill extraction using NLP PhraseMatcher, and deep semantic TF-IDF job description benchmarking.

---

## 🌟 Key Features

- **Multi-Format Document Parsing**: Ingests `.pdf` and `.docx` resumes (supporting files up to 50MB) using `pdfplumber` and `python-docx`.
- **Hybrid NLP Engine**:
  - **spaCy PhraseMatcher**: Exact, case-insensitive extraction of multi-word technical competencies (e.g. *Machine Learning*, *FastAPI*, *PySpark*) and industry certifications (e.g. *AWS Certified Solutions Architect*).
  - **TF-IDF & Cosine Similarity**: N-gram semantic vectorization to detect high-weight keywords and match percentages against target job descriptions.
  - **ATS Structural Hygiene**: Automatic detection of core sections, contact channels (email, phone, LinkedIn/GitHub), action verbs, quantifiable metrics, and optimal word count.
- **Glassmorphic Bento-Grid UI**:
  - Interactive Drag & Drop with immediate file size and type validation.
  - Multi-stage scanning milestone visualizer.
  - Dynamic animated SVG circular score gauge.
  - Segmented badges for matched skills, missing skills, and certifications.
  - Actionable feedback and optimization suggestions.

---

## 📁 Project Architecture

```
ats_checker/
├── app.py                  # Flask backend & routing
├── parser.py               # Text extraction for PDF & DOCX
├── analyzer.py             # Hygiene scoring & TF-IDF similarity engine
├── skills_extractor.py     # spaCy PhraseMatcher for skills & certifications
├── requirements.txt        # Project dependencies
├── templates/
│   └── index.html          # Glassmorphic UI & dashboard
├── static/                 # Static assets
└── uploads/                # Temporary file upload staging
```

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/ats-checker.git
cd ats-checker
```

### 2. Set Up Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 4. Run the Application
```bash
python app.py
```

Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🛠️ Tech Stack

- **Backend**: Python 3.11+, Flask, Werkzeug
- **NLP & ML**: spaCy (`en_core_web_sm`), scikit-learn (`TfidfVectorizer`, `cosine_similarity`)
- **Document Processing**: `pdfplumber`, `python-docx`
- **Frontend**: Vanilla HTML5/CSS3/JavaScript, Lucide Icons, Google Fonts
