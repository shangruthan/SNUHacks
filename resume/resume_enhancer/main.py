from groq import Groq

# Initialize Groq client
print("Initializing Groq client...")
client = Groq(api_key="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")  # Replace with your actual Groq API key
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
            {"role": "system", "content": "You are a professional resume enhancer. Your responses should only consist of the subheading and enhanced resume content for each subheading and nothing else."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1024,
    )
    print("Received response from Groq API.")

    # Debug: Print Groq API response
    print("Groq API Response:", completion.choices[0].message.content)
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

    # Path to the resume text file and job description
    resume_txt_path = "resume.txt"
    job_description_path = "job_description.txt"
    enhanced_resume_path = "enhanced.txt"  # Path to save enhanced resume

    # Load the resume content
    print("Loading resume...")
    with open(resume_txt_path, "r") as file:
        resume_content = file.read()
    print("Resume loaded successfully.")

    # Load the job description
    print("Loading job description...")
    with open(job_description_path, "r") as file:
        job_description = file.read()
    print("Job description loaded.")

    # Split the resume content into sections based on headings
    parsed_resume = {}
    current_heading = None
    for line in resume_content.splitlines():
        if line.strip() in headings:
            current_heading = line.strip()
            parsed_resume[current_heading] = []
        elif current_heading:
            parsed_resume[current_heading].append(line.strip())

    # Convert each section to a single string (paragraph)
    for heading, content in parsed_resume.items():
        parsed_resume[heading] = "\n".join(content)

    # Enhance each section
    enhanced_resume = {}
    for heading, content in parsed_resume.items():
        print(f"Processing section: {heading}")
        enhanced_resume[heading] = enhance_section(heading, content, job_description)
        print(f"Enhanced {heading}:\n{enhanced_resume[heading]}\n")

    # Print enhanced_resume dictionary for debugging
    print("Enhanced Resume Content:")
    with open(enhanced_resume_path, "w") as file:
        for heading, content in enhanced_resume.items():
             file.write(f"{heading}:\n{content}\n\n")

    # Save the enhanced resume to a file (similar to how it was done with Groq)
   

# Call the main function
if __name__ == "__main__":
    main()
