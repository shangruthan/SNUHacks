from transformers import pipeline

def extract_ats_keywords(parsed_job_description):
    """
    Extract ATS keywords from the parsed job description.
    """
    # Load a Hugging Face model for keyword extraction
    keyword_extractor = pipeline("text-generation", model="gpt2")
    
    # Extract keywords for each heading
    ats_keywords = {}
    for heading, content in parsed_job_description.items():
        prompt = f"Extract key skills and keywords from this {heading} section: {content}"
        keywords = keyword_extractor(prompt, max_new_tokens=50, num_return_sequences=1)[0]['generated_text']
        keywords = keywords.replace(prompt, "").strip().split(", ")
        ats_keywords[heading] = keywords
    
    return ats_keywords