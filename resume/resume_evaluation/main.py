# main.py
import os
from core import evaluate_resume

def read_parsed_file(file_path):
    """
    Read a parsed file (jd.txt or resume.txt) and return a dictionary with headings and content.
    
    :param file_path: Path to the parsed file.
    :return: Dictionary with headings as keys and content as values.
    """
    parsed_data = {}
    with open(file_path, "r", encoding="utf-8") as file:
        current_heading = None
        for line in file:
            line = line.strip()
            if line.endswith(":"):  # Detect headings
                current_heading = line[:-1]  # Remove the colon
                parsed_data[current_heading] = ""
            elif current_heading:  # Add content under the current heading
                parsed_data[current_heading] += line + "\n"
    return parsed_data

# Path to the job description file (jd.txt)
jd_path = "jd.txt"

# Path to the resume file (resume.txt)
resume_path = "resume.txt"

# Verify the files exist
if not os.path.exists(jd_path):
    print(f"Error: File '{jd_path}' not found in the current directory.")
elif not os.path.exists(resume_path):
    print(f"Error: File '{resume_path}' not found in the current directory.")
else:
    print(f"Files '{jd_path}' and '{resume_path}' found. Proceeding with evaluation...")

    # Read the job description from jd.txt
    job_description = read_parsed_file(jd_path)

    # Read the resume from resume.txt
    resume_data = read_parsed_file(resume_path)

    # Print job description and parsed resume data for debugging
    print("\nJob Description:")
    for section, text in job_description.items():
        print(f"{section}:\n{text}")

    print("\nParsed Resume Data:")
    for section, text in resume_data.items():
        print(f"{section}:\n{text}")

    # Evaluate the resume
    scores, aggregate_score = evaluate_resume(job_description, resume_data)

    # Print results
    print("\nScores for each section:")
    for section, score in scores.items():
        print(f"{section}: {score:.2f}")

    print(f"\nAggregate Score: {aggregate_score:.2f}")