from groq import Groq
from skills_gap_analyzer.resume import resume_information
from skills_gap_analyzer.job_description import jd

#from resume import resume_information
#from job_description import jd

# Initialize Groq client
print("Initializing Groq client...")
client = Groq(api_key="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")  # Replace with your actual Groq API key
print("Groq client initialized.")

def missing_skills(resume_information, jd):
    """
    Skill gap analyzer using the Groq API.
    """
    print("Identifying missing skills and suggestions...")
    prompt = f"""
    Understand the job description and requirements and identify all the skills and information my resume misses out on when compared to this job description.
    Suggest courses for missing skills or improvements that are required.

    Job Description:
    {jd}

    Resume:
    {resume_information}
    """

    print("Sending prompt to Groq API...")
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Use the specified model
            messages=[
                {"role": "system", "content": "You are a professional career advisor and resume analyzer. Your task is to analyze the provided job description and resume, identify missing skills, qualifications, and experience, and suggest actionable improvements such as courses, certifications, or additional experience needed to bridge the gap. Provide clear, concise, and practical advice tailored to the job role"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1024,
        )
        print("Received response from Groq API.")
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return None

def main():
    print("Starting main function...")

    # Call the missing_skills function with resume_information and jd
    suggestions = missing_skills(resume_information, jd)
    
    if suggestions:
        print("Saving suggestions and improvements to analysis.txt...")
        with open(r"resume\skills_gap_analyzer\analysis.txt", "w") as file:
            file.write("Suggestions and Improvements:\n\n")
            file.write(suggestions)
        print("Suggestions saved to analysis.txt.")
    else:
        print("No suggestions to save.")

if __name__ == "__main__":
    print("Starting script...")
    main()
    print("Script completed.")