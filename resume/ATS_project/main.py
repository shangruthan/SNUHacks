# main.py

import os
from jd import job_description
from resume_parser import parse_resume
from core import evaluate_resume

# Path to the resume PDF (in the same folder as main.py)
resume_path = r"SDE_resume.pdf"

# Verify the file existsls
if not os.path.exists(resume_path):
    print(f"Error: File '{resume_path}' not found in the current directory.")
else:
    print(f"File '{resume_path}' found. Proceeding with parsing...")

    # Get headings from the job description
    headings = list(job_description.keys())

    # Parse the resume
    resume_data = parse_resume(resume_path, headings)

    # Print job description and parsed resume data for debugging
    print("\nJob Description:")
    for section, text in job_description.items():
        print(f"{section}: {text}")

    print("\nParsed Resume Data:")
    for section, text in resume_data.items():
        print(f"{section}: {text}")

    # Evaluate the resume
    scores, aggregate_score = evaluate_resume(job_description, resume_data)

    # Print results
    print("\nScores for each section:")
    for section, score in scores.items():
        print(f"{section}: {score:.2f}")

    print(f"\nAggregate Score: {aggregate_score:.2f}")