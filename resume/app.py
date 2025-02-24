# SNUHacks/resume/ATS_project/app.py

from flask import Flask, request, render_template, redirect, url_for
import os
from resume_evaluation.jd import job_description
from resume_evaluation.resume_parser import parse_resume
from resume_evaluation.core import evaluate_resume
import sqlite3  # New import for database
import json  # New import for handling JSON

app = Flask(__name__)

# Path to the resume upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize the database
def init_db():
    conn = sqlite3.connect('scores.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS resume_scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        scores TEXT,
        aggregate_score REAL
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS job_roles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_title TEXT,
        job_description TEXT
    )''')  # New table for job roles
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

        # Fetch job roles from the database
        c.execute('SELECT job_title FROM job_roles')
        job_roles = c.fetchall()  # Fetch all job titles

        # Retrieve rankings from the database
        c.execute('SELECT filename, aggregate_score FROM resume_scores ORDER BY aggregate_score DESC')
        rankings = c.fetchall()  # Fetch all rankings
        conn.close()

        return render_template('results.html', scores=scores, aggregate_score=aggregate_score, rankings=rankings, job_roles=job_roles)

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

@app.route('/individual_results', methods=['POST'])
def individual_results():
    # Here you would normally process the uploaded files
    # For now, we will just redirect to the results page with placeholder values
    match_score = "0.7"  # Placeholder match score
    suggestions = [
        "Tailor your resume to the job description.",
        "Use keywords from the job description.",
        "Highlight relevant experiences."
    ]
    return render_template('individual_results.html', match_score=match_score, suggestions=suggestions)

@app.route('/company_dashboard', methods=['GET', 'POST'])
def company_dashboard():
    # Fetch job roles from the database
    conn = sqlite3.connect('scores.db')
    c = conn.cursor()
    c.execute('SELECT job_title FROM job_roles')
    job_roles = c.fetchall()  # Fetch all job titles
    conn.close()

    if request.method == 'POST':
        candidate_name = request.form.get('candidate_name')  # Get the candidate's name
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

            # Store the scores in the database with candidate name
            conn = sqlite3.connect('scores.db')
            c = conn.cursor()
            c.execute('INSERT INTO resume_scores (filename, scores, aggregate_score) VALUES (?, ?, ?)',
                      (candidate_name, str(scores), aggregate_score))  # Use candidate name as filename
            conn.commit()

            # Redirect to the results page
            return render_template('results.html', scores=scores, aggregate_score=aggregate_score, job_roles=job_roles)

    return render_template('company_dashboard.html', job_roles=job_roles)  # Pass job roles to the template

@app.route('/analytics', methods=['GET', 'POST'])
def analytics():
    conn = sqlite3.connect('scores.db')
    c = conn.cursor()
    c.execute('SELECT filename, scores, aggregate_score FROM resume_scores')
    rankings = c.fetchall()  # Fetch all rankings
    conn.close()

    # Prepare data for visualization
    filenames = [r[0] for r in rankings]
    aggregate_scores = [r[2] for r in rankings]
    individual_scores = [eval(r[1]) for r in rankings]  # Convert JSON string back to dictionary

    if request.method == 'POST':
        selected_files = request.form.getlist('candidates')
        selected_scores = {filename: individual_scores[i] for i, filename in enumerate(filenames) if filename in selected_files}
    else:
        selected_scores = {filenames[0]: individual_scores[0]}  # Default to the first candidate

    # Generate visualizations (example using Matplotlib)
    import matplotlib.pyplot as plt
    import io
    import base64

    # Create a smaller figure for the selected candidates
    fig, ax = plt.subplots(figsize=(8, 4))  # Adjusted size

    for filename, scores in selected_scores.items():
        sections = list(scores.keys())
        values = list(scores.values())
        ax.bar(sections, values, label=filename)

    ax.set_title('Individual Scores Comparison')
    ax.set_ylabel('Scores')
    ax.set_xticklabels(sections, rotation=45, ha='right')
    ax.legend()
    plt.tight_layout()

    # Save the plot to a BytesIO object and encode it to base64
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')  # Ensure tight layout
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('analytics.html', plot_url=plot_url, filenames=filenames)

@app.route('/add_job_role', methods=['GET', 'POST'])
def add_job_role():
    if request.method == 'POST':
        job_title = request.form.get('job_title')
        job_description_text = request.form.get('job_description')
        # Save the job role to the database
        conn = sqlite3.connect('scores.db')
        c = conn.cursor()
        c.execute('INSERT INTO job_roles (job_title, job_description) VALUES (?, ?)',
                  (job_title, job_description_text))
        conn.commit()
        conn.close()
        return redirect(url_for('view_job_roles'))

    return render_template('add_job_role.html')

@app.route('/view_job_roles', methods=['GET'])
def view_job_roles():
    conn = sqlite3.connect('scores.db')
    c = conn.cursor()
    c.execute('SELECT job_title, job_description FROM job_roles')
    job_roles = c.fetchall()  # Fetch all job roles
    conn.close()
    return render_template('view_job_roles.html', job_roles=job_roles)  # Pass job roles to the template

# Call the database initialization function
if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)