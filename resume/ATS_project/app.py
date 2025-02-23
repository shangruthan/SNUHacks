# SNUHacks/resume/ATS_project/app.py

from flask import Flask, request, render_template, redirect, url_for
import os
from jd import job_description
from parser import parse_resume
from core import evaluate_resume
import sqlite3  # New import for database

app = Flask(__name__)

# Path to the resume upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize the database
def init_db():
    conn = sqlite3.connect('scores.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS resume_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            scores TEXT,  -- Store scores as a JSON string
            aggregate_score REAL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return redirect(url_for('login'))  # Redirect to the login page

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

        # Store the scores in the database
        conn = sqlite3.connect('scores.db')
        c = conn.cursor()
        c.execute('INSERT INTO resume_scores (filename, scores, aggregate_score) VALUES (?, ?, ?)',
                  (file.filename, str(scores), aggregate_score))
        conn.commit()

        # Retrieve rankings from the database
        c.execute('SELECT filename, aggregate_score FROM resume_scores ORDER BY aggregate_score DESC')
        rankings = c.fetchall()  # Fetch all rankings
        conn.close()

        return render_template('results.html', scores=scores, aggregate_score=aggregate_score, rankings=rankings)

@app.route('/rankings')
def view_rankings():
    conn = sqlite3.connect('scores.db')
    c = conn.cursor()
    c.execute('SELECT filename, scores, aggregate_score FROM resume_scores ORDER BY aggregate_score DESC')
    rankings = c.fetchall()  # Fetch all rankings
    conn.close()

    # Convert scores from JSON string to dictionary
    for i in range(len(rankings)):
        filename, scores_json, aggregate_score = rankings[i]
        scores = eval(scores_json)  # Convert JSON string back to dictionary
        rankings[i] = (filename, scores, aggregate_score)  # Update the tuple

    return render_template('rankings.html', rankings=rankings)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_type = request.form.get('user_type')
        if user_type == 'individual':
            return redirect(url_for('individual_dashboard'))
        elif user_type == 'company':
            return redirect(url_for('company_dashboard'))
    return render_template('login.html')

@app.route('/individual_dashboard')
def individual_dashboard():
    return render_template('individual_dashboard.html')

@app.route('/company_dashboard', methods=['GET', 'POST'])
def company_dashboard():
    if request.method == 'POST':
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

            # Store the scores in the database
            conn = sqlite3.connect('scores.db')
            c = conn.cursor()
            c.execute('INSERT INTO resume_scores (filename, scores, aggregate_score) VALUES (?, ?, ?)',
                      (file.filename, str(scores), aggregate_score))
            conn.commit()

            # Redirect to the results page
            return render_template('results.html', scores=scores, aggregate_score=aggregate_score)

    return render_template('company_dashboard.html')

# Call the database initialization function
if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)