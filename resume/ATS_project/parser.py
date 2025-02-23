# parser.py

from transformers import pipeline
from PyPDF2 import PdfReader

# Load a zero-shot classification model
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

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