# resume/resume_evaluation/parse_job_description.py

import os
import sys

# Add the utils folder to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

from job_description_parser import parse_job_description, save_job_description

# Define the headings for job description parsing
headings = [
    "Education",
    "Experience",
    "Skills",
    "Projects",
    "Certifications",
]

# Path to the job description file
job_description_file = os.path.join(os.path.dirname(__file__), "job_description.txt")

# Path to save the parsed job description
output_file = os.path.join(os.path.dirname(__file__), "jd.txt")

# Check if the job description file exists
if not os.path.exists(job_description_file):
    print(f"Error: The file '{job_description_file}' does not exist.")
else:
    # Read the job description text
    with open(job_description_file, "r", encoding="utf-8") as file:
        job_description_text = file.read()

    # Parse the job description
    job_description_data = parse_job_description(job_description_text, headings)

    # Save the parsed job description to a file
    save_job_description(job_description_data, output_file)