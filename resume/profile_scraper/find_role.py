import os
import sys

# Add parent directory (resume/) to Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from utils import groq_utils

def read_job_description(file_path):
    """Read job description from text file"""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return None

def extract_job_info(jd_text):
    """Extract job role and company using Groq API"""
    groq_client = groq_utils.GroqClient(api_key="")  # Add your Groq API key here
    
    system_msg = """You are an expert HR analyst. Extract and return only:
    1. Job role/title
    2. Company name
    From the provided job description. Use exact wording from the text.
    Format response as: Role: [role]\nCompany: [company]"""
    
    response = groq_client.send_prompt(
        system_message=system_msg,
        user_prompt=f"Job Description:\n{jd_text}"
    )
    
    return parse_groq_response(response)

def parse_groq_response(response):
    """Parse Groq response into structured data"""
    result = {"role": "Not specified", "company": "Not specified"}
    
    if response:
        for line in response.split('\n'):
            if line.startswith('Role:'):
                result['role'] = line.replace('Role:', '').strip()
            elif line.startswith('Company:'):
                result['company'] = line.replace('Company:', '').strip()
    
    return result

def main():
    # Configuration
    jd_path = os.path.join(os.path.dirname(__file__), "job_description.txt")
    
    # Check file exists
    if not os.path.exists(jd_path):
        print(f"Error: Job description file not found at {jd_path}")
        return
    
    # Read job description
    jd_text = read_job_description(jd_path)
    if not jd_text:
        return
    
    # Extract information
    job_info = extract_job_info(jd_text)
    
    # Display results
    print("\nJob Information Extraction Results:")
    print(f"Role: {job_info['role']}")
    print(f"Company: {job_info['company']}")

    return job_info  # Return the job_info dictionary

if __name__ == "__main__":
    main()