# resume/skill_gap_analyzer/missing_skills.py

import os
import sys
from transformers import pipeline
# Add the utils folder to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

from groq_utils import GroqClient
from skills_gap_analyzer.resume import resume_information
from skills_gap_analyzer.job_description import job_description

# Load the zero-shot classification model
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def analyze_missing_skills(resume_info, job_desc, output_file="analysis.txt"):
    """
    Analyze missing skills between the resume and job description using Groq API.
    
    :param resume_info: The resume information.
    :param job_desc: The job description.
    :param output_file: The file to save the analysis results (saved in the same folder as this script).
    """
    # Initialize Groq client
    groq_client = GroqClient(api_key="your_groq_api_key_here")

    # Define the system message and user prompt
    system_message = "You are a professional career advisor and resume analyzer. Your task is to analyze the provided job description and resume, identify missing skills, qualifications, and experience, and suggest actionable improvements such as courses, certifications, or additional experience needed to bridge the gap. Provide clear, concise, and practical advice tailored to the job role."
    
    user_prompt = f"""
    Understand the job description and requirements and identify all the skills and information my resume misses out on when compared to this job description.
    Suggest courses for missing skills or improvements that are required.

    Job Description:
    {job_desc}

    Resume:
    {resume_info}
    """

    # New prompt to identify the job role
    job_role_prompt = f"""
    Identify the job role from the following job description:
    
    Job Description:
    {job_desc}
    In your Reply provide only the name of the role and nothing else.
    """

    # Send the prompts to Groq API
    print("Sending prompts to Groq API...")
    suggestions = groq_client.send_prompt(system_message, user_prompt)
    job_role = groq_client.send_prompt(system_message, job_role_prompt)
    
    if suggestions:
        # Save the output file in the same folder as this script
        output_path = os.path.join(os.path.dirname(__file__), output_file)
        print(f"Saving suggestions and improvements to {output_path}...")
        with open(output_path, "w") as file:
            file.write("Suggestions and Improvements:\n\n")
            file.write(suggestions)
        print(f"Suggestions saved to {output_path}.")
    else:
        print("No suggestions to save.")
    
    # Output only the identified job role
    print(job_role)
    
    candidate_roles = [
    "Frontend",
    "Backend",
    "Full Stack",
    "AI Engineer",
    "Data Analyst",
    "Cyber Security",
    "Software Architect",
    "Game Developer",
    "Product Manager",
    "Technical Writer",
    "Engineering Manager",
    "DevOps",
    "AI and Data Scientist",
    "Android",
    "Blockchain",
    "iOS",
    "QA",
    "UX Design",
    "MLOps",
    "Developer Relations"
]
    
    # Classify the identified role against the candidate roles
    result = classifier(job_role, candidate_roles)

    # Get the best matching role
    best_matching_role = result['labels'][0]
    print(f"The best matching role is: {best_matching_role}")
    
    return suggestions, best_matching_role

if __name__ == "__main__":
    print("Starting missing skills analysis...")
    analyze_missing_skills(resume_information, job_description)
    print("Analysis completed.")