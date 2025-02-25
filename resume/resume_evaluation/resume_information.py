# resume/resume_evaluation/resume_information.py

import os
import sys

# Add the utils folder to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

from resume_parser import parse_resume

# Path to the resume PDF
pdf_path = "resume_Rejen.pdf"  # Replace with the actual path to your resume PDF

# Output folder (same as the current folder)
output_folder = os.path.dirname(__file__)

# Parse the resume and save the output
output_file = parse_resume(pdf_path, output_folder)

print(f"Resume parsed and saved to: {output_file}")