from groq import Groq
from parser import parse_resume

# Initialize Groq client
print("Initializing Groq client...")
client = Groq(api_key="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")
print("Groq client initialized.")

def enhance_section(heading, content, job_description):
    """
    Enhances a resume section using the Groq API.
    """
    print(f"Enhancing section: {heading}")
    prompt = f"""
    Enhance the following resume section to make it ATS-friendly and highly relevant to the job description.
    Focus on incorporating keywords and requirements from the job description while maintaining clarity and professionalism.

    Job Description:
    {job_description}

    Resume Section ({heading}):
    {content}

    Enhanced Resume Section:
    """

    print("Sending prompt to Groq API...")
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Use the specified model
        messages=[
            {"role": "system", "content": "You are a professional resume enhancer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1024,
    )
    print("Received response from Groq API.")

    return completion.choices[0].message.content

def main():
    print("Starting main function...")

    # Define predefined headings
    headings = [
        "Education",
        "Work Experience",
        "Projects",
        "Technical Skills",
        "Certifications",
        "Event Participation and Awards"
    ]

    # Path to the resume PDF and job description
    resume_pdf_path = "SDE_resume.pdf"
    job_description_path = "job_description.txt"
    enhanced_resume_path = "enhanced.txt"

    # Parse the resume
    print("Parsing resume...")
    parsed_resume = parse_resume(resume_pdf_path, headings)
    print("Resume parsed successfully.")

    # Load the job description
    print("Loading job description...")
    with open(job_description_path, "r") as file:
        job_description = file.read()
    print("Job description loaded.")

    # Enhance each section
    enhanced_resume = {}
    for heading, content in parsed_resume.items():
        print(f"Processing section: {heading}")
        enhanced_resume[heading] = enhance_section(heading, content, job_description)
        print(f"Enhanced {heading}:\n{enhanced_resume[heading]}\n")

    # Save the enhanced resume to a file
    print("Saving enhanced resume...")
    with open(enhanced_resume_path, "w") as file:
        for heading, content in enhanced_resume.items():
            file.write(f"{heading}:\n{content}\n\n")
    print(f"Enhanced resume saved to '{enhanced_resume_path}'.")

if __name__ == "__main__":
    print("Starting script...")
    main()
    print("Script completed.")