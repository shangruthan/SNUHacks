# resume/utils/job_description_parser.py

from transformers import pipeline
import torch

def parse_job_description(job_description_text, headings):
    """
    Parse a job description text and categorize it into predefined headings.
    
    :param job_description_text: The raw job description text.
    :param headings: List of headings to categorize the job description content.
    :return: A dictionary with categorized job description content.
    """
    # Check if GPU is available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    # Load a zero-shot classification model
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=0 if device == "cuda" else -1)

    # Split text into sentences or paragraphs
    paragraphs = job_description_text.split("\n")  # Split by newlines (adjust as needed)

    # Classify each paragraph into one of the predefined headings
    job_description_data = {heading: "" for heading in headings}
    for paragraph in paragraphs:
        if paragraph.strip():  # Skip empty paragraphs
            # Classify the paragraph
            result = classifier(paragraph, headings)
            best_match = result["labels"][0]  # Get the best matching heading
            job_description_data[best_match] += paragraph + "\n"

    return job_description_data

def save_job_description(job_description_data, output_file):
    """
    Save the parsed job description data to a .txt file.
    
    :param job_description_data: The parsed job description data (dictionary).
    :param output_file: The file to save the parsed data.
    """
    with open(output_file, "w", encoding="utf-8") as file:
        for heading, data in job_description_data.items():
            file.write(f"{heading}:\n{data}\n\n")

    print(f"Job description parsed and saved to {output_file}.")