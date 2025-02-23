from transformers import pipeline

# Load a Hugging Face model for text generation
generator = pipeline("text-generation", model="distilgpt2")  # Use a smaller model

def enhance_resume(parsed_resume, ats_keywords):
    """
    Enhance the resume based on the extracted ATS keywords.
    """
    enhanced_resume = {}
    for heading, content in parsed_resume.items():
        if heading == "Work Experience":
            enhanced_content = enhance_work_experience(content, ats_keywords.get("Experience", []))
        elif heading == "Skills":
            enhanced_content = enhance_skills(content, ats_keywords.get("Skills", []))
        elif heading == "Education":
            enhanced_content = enhance_education(content, ats_keywords.get("Education", []))
        else:
            enhanced_content = content
        enhanced_resume[heading] = enhanced_content
    return enhanced_resume

def enhance_work_experience(content, experience_keywords):
    """
    Enhance the "Work Experience" section without adding false information.
    """
    enhanced_content = []
    for item in content.split("\n"):
        if item.strip():  # Skip empty lines
            # Use a constrained prompt to avoid hallucinations
            prompt = f"Rephrase the following work experience to make it more professional and ATS-friendly, without adding new information: {item}"
            improved_item = generator(prompt, max_new_tokens=50, num_return_sequences=1)[0]['generated_text']
            # Filter out any irrelevant content
            improved_item = improved_item.replace(prompt, "").strip()
            enhanced_content.append(improved_item)
    return "\n".join(enhanced_content)

def enhance_skills(content, skills_keywords):
    """
    Enhance the "Skills" section without adding false information.
    """
    enhanced_content = []
    for skill in content.split("\n"):
        if skill.strip():  # Skip empty lines
            # Use a constrained prompt to avoid hallucinations
            prompt = f"Rephrase the following skill to make it more professional and ATS-friendly, without adding new information: {skill}"
            improved_skill = generator(prompt, max_new_tokens=20, num_return_sequences=1)[0]['generated_text']
            # Filter out any irrelevant content
            improved_skill = improved_skill.replace(prompt, "").strip()
            enhanced_content.append(improved_skill)
    return "\n".join(enhanced_content)

def enhance_education(content, education_keywords):
    """
    Enhance the "Education" section without adding false information.
    """
    enhanced_content = []
    for item in content.split("\n"):
        if item.strip():  # Skip empty lines
            # Use a constrained prompt to avoid hallucinations
            prompt = f"Rephrase the following education detail to make it more professional and ATS-friendly, without adding new information: {item}"
            improved_item = generator(prompt, max_new_tokens=30, num_return_sequences=1)[0]['generated_text']
            # Filter out any irrelevant content
            improved_item = improved_item.replace(prompt, "").strip()
            enhanced_content.append(improved_item)
    return "\n".join(enhanced_content)