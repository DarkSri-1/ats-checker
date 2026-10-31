import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from parser import extract_text
from analyzer import analyze_without_jd, analyze_with_jd

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB

ALLOWED_EXTENSIONS = {'pdf', 'docx'}
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files:
        return jsonify({'error': 'No resume file provided'}), 400

    file = request.files['resume']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid format. Only .pdf and .docx allowed'}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    try:
        resume_text = extract_text(file_path)
        jd_text = request.form.get('jd_text', '').strip()

        if jd_text:
            result = analyze_with_jd(resume_text, jd_text)
            result['mode'] = 'with_jd'
        else:
            result = analyze_without_jd(resume_text)
            result['mode'] = 'without_jd'

        return jsonify(result)
    except Exception as err:
        return jsonify({'error': str(err)}), 500
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)  # Clean up uploaded file

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({'error': 'File exceeds maximum upload size of 50MB'}), 413

if __name__ == '__main__':
    app.run(debug=True, port=5000)
