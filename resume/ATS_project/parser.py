# parser.py

from transformers import pipeline
from PyPDF2 import PdfReader
import torch
print(torch.cuda.is_available())  # Should return True if CUDA is enabled
print(torch.cuda.get_device_name(0))  # Should return the name of your GPU


# Check if GPU is available
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Load a zero-shot classification model and move it to the GPU
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=0 if device == "cuda" else -1)


def parse_resume(pdf_path, headings):
    """
    Parse a resume PDF and categorize text into predefined headings.
    """
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

    # Print parsed data for debugging
    print("\nParsed Resume Data:")
    for heading, data in resume_data.items():
        print(f"{heading}: {data}")

    return resume_data