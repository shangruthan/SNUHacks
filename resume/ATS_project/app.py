# SNUHacks/resume/ATS_project/app.py

from flask import Flask, request, render_template
import os
from jd import job_description
from parser import parse_resume
from core import evaluate_resume

app = Flask(__name__)

# Path to the resume upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'resume' not in request.files:
        return "No file part"
    file = request.files['resume']
    if file.filename == '':
        return "No selected file"
    if file:
        resume_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(resume_path)

        # Get headings from the job description
        headings = list(job_description.keys())

        # Parse the resume
        resume_data = parse_resume(resume_path, headings)

        # Evaluate the resume
        scores, aggregate_score = evaluate_resume(job_description, resume_data)

        return render_template('results.html', scores=scores, aggregate_score=aggregate_score)

if __name__ == '__main__':
    app.run(debug=True)