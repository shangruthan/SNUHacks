from utils.parser import parse_resume  # Reuse the existing parser
from utils.job_description_parser import parse_job_description
from utils.keyword_extractor import extract_ats_keywords
from utils.enhancer import enhance_resume
from utils.file_utils import save_enhanced_resume_txt

def main():
    # Paths to resume and job description
    resume_path = "SDE_resume.pdf"  # Resume file in the same folder as main.py
    job_description_path = "job_description.txt"  # Job description file in the same folder as main.py
    
    # Predefined headings for the resume
    headings = ["Work Experience", "Skills", "Education", "Projects", "Summary"]
    
    # Parse resume
    parsed_resume = parse_resume(resume_path, headings)
    
    # Parse and summarize job description
    with open(job_description_path, "r") as f:
        job_description = f.read()
    parsed_job_description = parse_job_description(job_description)
    
    # Extract ATS keywords from the parsed job description
    ats_keywords = extract_ats_keywords(parsed_job_description)
    
    # Enhance resume
    enhanced_resume = enhance_resume(parsed_resume, ats_keywords)
    
    # Save enhanced resume as .txt
    output_txt_path = "enhanced_resume.txt"
    save_enhanced_resume_txt(enhanced_resume, output_txt_path)

if __name__ == "__main__":
    main()