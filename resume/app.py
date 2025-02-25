# SNUHacks/resume/ATS_project/app.py

from flask import Flask, request, render_template, redirect, url_for, jsonify
import os
import uuid
from werkzeug.utils import secure_filename
from resume_evaluation.job_description import job_description
from utils.resume_parser import parse_resume
from resume_evaluation.core import evaluate_resume
import sqlite3  # New import for database
import json  # New import for handling JSON
from skills_gap_analyzer.main import analyze_missing_skills
from skills_gap_analyzer.resume import resume_information
from resume_evaluation.job_description import job_description
from resume_enhancer.main import enhance_section
import markdown  # Import the markdown library
from groq_utils import GroqClient  # New import for Groq client

# Import additional libraries from portfolio.py
from PyPDF2 import PdfReader
from groq import Groq

app = Flask(__name__)

# Path to the resume upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize Groq API client
groq_client = GroqClient(api_key="Placeholder")  # Replace with your actual API key

# Helper function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

# Functions from portfolio.py for file parsing
def read_pdf(file_path):
    try:
        pdf_reader = PdfReader(file_path)
        text = '\n'.join([page.extract_text() or '' for page in pdf_reader.pages])
        return text.strip()
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None


def parse_resume_file(file_path):
    ext = file_path.rsplit('.', 1)[-1].lower()
    if ext == 'pdf':
        return read_pdf(file_path)
    else:
        print("OnlyPDFs")
    return None

def process_resume_with_groq(text):
    try:
        response = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": """
                    You are an AI that extracts highly detailed and structured resume information in JSON format. 
                    Your output should be a structured JSON object with the following fields:
                    {
                        "name": "Full Name",
                        "headline": "Short Professional Title",
                        "summary": "A detailed bio about the user (3-5 sentences highlighting key skills, achievements, and career goals)",
                        "experience": [
                            {
                                "position": "Job Title",
                                "company": "Company Name",
                                "location": "City, Country",
                                "duration": "Start Date - End Date",
                                "description": [
                                    "Detailed description of responsibilities (3-5 bullet points)",
                                    "Key achievements (e.g., 'Increased sales by 20%', 'Reduced system downtime by 30%')",
                                    "Technologies/tools used (e.g., 'Python, React, AWS')"
                                ],
                                "projects": [
                                    {
                                        "name": "Project Name",
                                        "description": "Detailed description of the project (3-5 bullet points)",
                                        "technologies": ["Tech1", "Tech2", "Tech3"],
                                        "outcome": "Key outcomes or impact of the project"
                                    }
                                ]
                            }
                        ],
                        "education": [
                            {
                                "degree": "Degree Name",
                                "institution": "University Name",
                                "location": "City, Country",
                                "duration": "Start Date - End Date",
                                "gpa": "GPA (if available)",
                                "courses": ["Course1", "Course2", "Course3"],
                                "achievements": [
                                    "Notable achievements (e.g., 'Dean's List', 'Scholarship Recipient')"
                                ],
                                "thesis": "Thesis Title (if applicable)",
                                "extracurriculars": [
                                    "Extracurricular activities (e.g., 'President of Coding Club')"
                                ]
                            }
                        ],
                        "skills": {
                            "technical": ["Skill1", "Skill2", "Skill3"],
                            "soft": ["Skill1", "Skill2", "Skill3"],
                            "tools": ["Tool1", "Tool2", "Tool3"],
                            "languages": ["Language1", "Language2"]
                        },
                        "projects": [
                            {
                                "name": "Project Title",
                                "description": "Detailed description of the project (3-5 bullet points)",
                                "technologies": ["Tech1", "Tech2", "Tech3"],
                                "outcome": "Key outcomes or impact of the project",
                                "duration": "Start Date - End Date",
                                "role": "Role in the project (e.g., 'Team Lead', 'Developer')",
                                "link": "Project URL (if available)"
                            }
                        ],
                        "courses_and_certifications": [
                            {
                                "name": "Course/Certification Name",
                                "issuer": "Issuing Organization",
                                "duration": "Start Date - End Date",
                                "description": "Brief description of the course/certification",
                                "skills_gained": ["Skill1", "Skill2", "Skill3"]
                            }
                        ],
                        "achievements": [
                            {
                                "title": "Achievement Title",
                                "description": "Detailed description of the achievement",
                                "year": "Year of Achievement",
                                "issuer": "Issuing Organization (if applicable)"
                            }
                        ],
                        "events": [
                            {
                                "name": "Event Name",
                                "description": "Detailed description of the event",
                                "role": "Role in the event (e.g., 'Speaker', 'Organizer')",
                                "year": "Year of Event",
                                "location": "City, Country"
                            }
                        ],
                        "contact": {
                            "email": "email@example.com",
                            "phone": "Phone Number",
                            "location": "City, Country",
                            "linkedin": "LinkedIn URL",
                            "github": "GitHub URL",
                            "portfolio": "Personal Portfolio URL"
                        }
                    }
                    Respond ONLY with valid JSON and no extra text.
                """},
                {"role": "user", "content": text}
            ],
            model="llama-3.3-70b-versatile"
        )

        response_data = response.choices[0].message.content.strip()

        try:
            parsed_data = json.loads(response_data)
            return parsed_data
        except json.JSONDecodeError:
            print("🚨 JSON Decode Error! Attempting cleanup...")
            start_idx = response_data.find("{")
            end_idx = response_data.rfind("}") + 1
            if start_idx != -1 and end_idx != -1:
                cleaned_json = response_data[start_idx:end_idx]
                return json.loads(cleaned_json)
            return {"error": "Invalid JSON response", "details": response_data}

    except Exception as e:
        print(f"Groq API error: {e}")
        return {"error": str(e)}

@app.route('/')
def home():
    return redirect(url_for('login'))  # Redirect to the login page

@app.route('/generate_portfolio')
def portfolio_generator():
    return render_template('generate_portfolio.html')

@app.route('/portfolio-upload', methods=['POST'])
def portfolio_upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{uuid.uuid4()}_{filename}")
    file.save(file_path)
    
    resume_text = parse_resume_file(file_path)
    if not resume_text:
        os.remove(file_path)
        return jsonify({'error': 'Failed to extract text'}), 500
    
    parsed_resume = process_resume_with_groq(resume_text)
    os.remove(file_path)
    
    if 'error' in parsed_resume:
        return jsonify(parsed_resume), 500
    
    return render_template('modern_portfolio.html', data=parsed_resume)

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

@app.route('/enhance_resume', methods=['GET', 'POST'])
def enhance_resume():
    if request.method == 'POST':
        # Load the job description
        job_description_path = "resume/resume_enhancer/job_description.txt"
        with open(job_description_path, "r", encoding='utf-8') as file:
            job_description = file.read()

        # Load the hardcoded resume content
        resume_txt_path = "resume/resume_enhancer/resume.txt"  # Path to your hardcoded resume
        print("Loading resume...")
        with open(resume_txt_path, "r", encoding='utf-8') as file:
            resume_content = file.read()
        print("Resume loaded successfully.")

        # Define predefined headings
        headings = [
            "Education",
            "Work Experience",
            "Projects",
            "Technical Skills",
            "Certifications",
            "Event Participation and Awards"
        ]

        # Split the resume content into sections based on headings
        parsed_resume = {}
        current_heading = None
        for line in resume_content.splitlines():
            line = line.strip()  # Remove leading/trailing whitespace
            if line in headings:
                current_heading = line
                if current_heading not in parsed_resume:  # Prevent duplicate headings
                    parsed_resume[current_heading] = []
            elif current_heading:
                parsed_resume[current_heading].append(line)

        # Convert each section to a single string (paragraph)
        for heading, content in parsed_resume.items():
            parsed_resume[heading] = "\n".join(content)

        # Enhance each section
        enhanced_resume = {}
        for heading, content in parsed_resume.items():
            print(f"Processing section: {heading}")
            enhanced_content = enhance_section(heading, content, job_description)
            if heading not in enhanced_resume:  # Prevent saving the same heading twice
                enhanced_resume[heading] = enhanced_content
            print(f"Enhanced {heading}:\n{enhanced_resume[heading]}\n")

        # Save the enhanced resume to a file
        enhanced_resume_path = "enhanced_resume.txt"  # Path to save enhanced resume
        with open(enhanced_resume_path, "w", encoding='utf-8') as file:
            for content in enhanced_resume.values():
                file.write(f"{content}\n\n")  # Write only the enhanced content

        # Redirect to the enhanced results page
        return redirect(url_for('enhanced_results'))

    return render_template('enhance_resume.html')

@app.route('/enhanced_results', methods=['GET'])
def enhanced_results():
    # Read the enhanced resume content from the file
    enhanced_resume_path = "enhanced_resume.txt"  # Path to the enhanced resume file
    with open(enhanced_resume_path, "r", encoding='utf-8') as file:
        enhanced_resume_content = file.read()
    enhanced_resume_content = markdown.markdown(enhanced_resume_content)
    return render_template('enhanced_results.html', enhanced_resume_content=enhanced_resume_content)

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
    # For now, we will use the existing resume and job description for analysis
    suggestions, job_role = analyze_missing_skills(resume_information, job_description)
    print(suggestions)  # Print the Groq response in the terminal
    # Get suggestions from the skills gap analyzer
    match_score = "0.7"  # Placeholder match score (you can calculate this based on the analysis if needed)
    # Save the Groq response to the analysis.txt file
    with open('resume/skills_gap_analyzer/analysis.txt', 'w') as file:
        file.write(suggestions)
   
    # Read the content of analysis.txt
    with open('resume/skills_gap_analyzer/analysis.txt', 'r') as file:
        analysis_content = file.read()  # Read the entire content of the file

    # Convert the Markdown content to HTML
    analysis_content_html = markdown.markdown(analysis_content)

    return render_template('individual_results.html', match_score=match_score, suggestions=suggestions, analysis_content=analysis_content_html, job_role=job_role)  # Pass job role to the template

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

def extract_suggestions():
    with open('resume/skills_gap_analyzer/analysis.txt', 'r') as file:
        content = file.read()
        
        # Split the content to find the "Actionable Improvements" section
        sections = content.split("Actionable Improvements:")
        if len(sections) > 1:
            suggestions_section = sections[1]
            # Split by newlines and filter out empty lines
            suggestions = [line.strip() for line in suggestions_section.splitlines() if line.strip()]
            return suggestions
        return []  # Return an empty list if no suggestions found

# Route to display job listings
@app.route('/job_listings')
def job_listings():
    try:
        with open(r'resume\job_opening\job_listings.json', 'r') as file:
            jobs = json.load(file)
    except Exception as e:
        print(f"Error loading job listings: {e}")
        jobs = []

    return render_template('job_listings.html', jobs=jobs)

@app.route('/skill_gap_analysis')
def skill_gap_analysis():
    return render_template('skill_gap_analysis.html')

@app.route('/scrape_linkedin')
def scrape_linkedin():
    return render_template('scrape_linkedin.html')

@app.route('/generate_resume', methods=['POST'])
def generate_resume():
    linkedin_url = request.form['linkedin_url']
    
    # Here you would call your scraping function to extract data from the LinkedIn profile
    # For example:
    # resume_data = scrape_linkedin_profile(linkedin_url)
    
    # After scraping, you can render a resume template with the extracted data
    # return render_template('resume.html', resume=resume_data)

    # Placeholder response for now
    return f"Scraping LinkedIn profile at: {linkedin_url}"

@app.route('/resume_evaluation')
def resume_evaluation():
    # Assuming job_roles is a list of job roles you want to display in the dropdown
    return render_template('resume_evaluation.html',)

@app.route('/generate_interview_questions', methods=['GET', 'POST'])
def generate_interview_questions():
    default_job_role  ="cybersecurity analyst"
    if request.method == 'POST':
        job_role = request.form.get('job_role')  # Get the job role from the form
        if not job_role:
            job_role = default_job_role
        # Define the system message for Groq API
        system_message = "You are a professional recruiter. Generate a list of interview questions for the following job role."

        # Define the user prompt
        user_prompt = f"""
        Generate a list of interview questions for the job role: {job_role}.
        Provide a variety of questions including technical, behavioral, and situational questions.
        """

        # Initialize Groq client
        groq_client = GroqClient(api_key="your_groq_api_key_here")  # Ensure to replace with your actual API key

        # Send the prompts to Groq API
        print("Sending prompts to Groq API...")
        questions = groq_client.send_prompt(system_message, user_prompt)
        questions_html  = markdown.markdown(questions)
        print(questions_html)
        if questions:
            return render_template('interview_questions.html', job_role=job_role, questions=questions_html)  # Render the questions in a new template
        else:
            return "No questions generated."

    return render_template('generate_interview_questions.html')  # Render the form for input

# Call the database initialization function
if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)