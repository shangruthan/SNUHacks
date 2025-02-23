from transformers import pipeline

def parse_job_description(job_description):
    """
    Parse the job description into meaningful headings and summarize it.
    """
    # Load a Hugging Face model for summarization
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    
    # Summarize the job description to capture the essence
    summary = summarizer(job_description, max_length=100, min_length=30, do_sample=False)[0]['summary_text']
    
    # Load a Hugging Face model for text classification (to extract headings)
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    
    # Define potential headings
    headings = ["Skills", "Experience", "Education", "Requirements", "Responsibilities"]
    
    # Classify the summary into headings
    parsed_job_description = {}
    for heading in headings:
        result = classifier(summary, candidate_labels=[heading])
        if result["scores"][0] > 0.5:  # Threshold for relevance
            parsed_job_description[heading] = summary
    
    return parsed_job_description