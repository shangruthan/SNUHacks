# core.py

from sentence_transformers import SentenceTransformer, util

# Define weights for each section
WEIGHTS = {
    "Work Experience": 0.4,
    "Technical Skills": 0.3,
    "Education": 0.1,
    "Certifications": 0.1,
    "Projects": 0.1
}

# Load a pre-trained Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def compare_text(jd_text, resume_text):
    """
    Compare two texts using Sentence Transformers.
    """
    if not jd_text.strip() or not resume_text.strip():
        print(f"Warning: Empty text detected. JD: '{jd_text}', Resume: '{resume_text}'")
        return 0.0  # Return 0 if either text is empty

    # Print texts being compared for debugging
    print(f"\nComparing Job Description and Resume Text:")
    print(f"Job Description: {jd_text}")
    print(f"Resume Text: {resume_text}")

    # Encode the texts into embeddings
    jd_embedding = model.encode(jd_text, convert_to_tensor=True)
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)

    # Compute cosine similarity between the embeddings
    
    similarity = util.cos_sim(jd_embedding, resume_embedding)
    print(f"Similarity Score: {similarity.item()}")
    return similarity.item()  # Convert tensor to a Python float

def calculate_scores(job_description, resume_data):
    """
    Calculate scores for each section based on the job description.
    """
    scores = {}
    for section, jd_text in job_description.items():
        resume_text = resume_data.get(section, "")
        scores[section] = compare_text(jd_text, resume_text)
    return scores

def calculate_aggregate_score(scores):
    """
    Calculate the aggregate score using predefined weights.
    """
    aggregate_score = 0
    for section, score in scores.items():
        if section in WEIGHTS:  # Check if the section exists in WEIGHTS
            aggregate_score += score * WEIGHTS[section]
    return aggregate_score

def evaluate_resume(job_description, resume_data):
    """
    Evaluate a resume against the job description.
    """
    scores = calculate_scores(job_description, resume_data)
    aggregate_score = calculate_aggregate_score(scores)
    return scores, aggregate_score