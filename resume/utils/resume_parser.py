# resume/utils/resume_parser.py

from PyPDF2 import PdfReader
from transformers import pipeline
import torch
import os

def parse_resume(pdf_path, output_folder):
    """
    Parse a resume PDF and save the extracted text into a .txt file.
    
    :param pdf_path: Path to the resume PDF file.
    :param output_folder: Folder where the output .txt file will be saved.
    :return: Path to the saved .txt file.
    """
    # Define the headings for resume parsing
    headings = ["Education", "Experience", "Skills", "Projects", "Certifications"]

    # Check if GPU is available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    # Load a zero-shot classification model
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=0 if device == "cuda" else -1)

    # Extract text from PDF
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    # Print extracted text for debugging
    print("Extracted Text from Resume:")
    print(text)

    # Split text into sentences or paragraphs
    paragraphs = text.split("\n")  # Split by newlines (adjust as needed)

    # Classify each paragraph into one of the predefined headings
    resume_data = {heading: "" for heading in headings}
    for paragraph in paragraphs:
        if paragraph.strip():  # Skip empty paragraphs
            # Classify the paragraph
            result = classifier(paragraph, headings)
            best_match = result["labels"][0]  # Get the best matching heading
            resume_data[best_match] += paragraph + "\n"

    # Save the parsed data to a .txt file
    output_path = os.path.join(output_folder, "resume.txt")
    with open(output_path, "w", encoding="utf-8") as file:  # Use UTF-8 encoding
        for heading, data in resume_data.items():
            file.write(f"{heading}:\n{data}\n\n")

    print(f"Resume parsed and saved to {output_path}.")
    return output_path