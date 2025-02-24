import os
import time
import json
import requests
import spacy
import nltk
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import PyPDF2
import docx

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Load NLP model
nlp = spacy.load("en_core_web_sm")


# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text


# Function to extract text from a DOCX file
def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])


# Function to extract skills dynamically using NLP
def extract_skills(resume_text):
    # Tokenize and remove stopwords
    words = word_tokenize(resume_text)
    words = [word.lower() for word in words if word.isalnum()]
    words = [word for word in words if word not in stopwords.words("english")]

    # Use Spacy NER to extract named entities (skills, technologies, certifications)
    doc = nlp(resume_text)
    extracted_skills = [ent.text.lower() for ent in doc.ents if ent.label_ in ["ORG", "PRODUCT", "WORK_OF_ART"]]

    # Merge NLTK and Spacy results
    extracted_skills = list(set(extracted_skills + words))
    
    return extracted_skills


# Function to search job postings on LinkedIn
def search_jobs_on_linkedin(query):
    job_list = []
    url = f"https://www.linkedin.com/jobs/search/?keywords={query.replace(' ', '%20')}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        soup = BeautifulSoup(response.text, "html.parser")

        jobs = soup.find_all("div", class_="base-search-card__info")

        for job in jobs[:50]:  # Limit to top 50 jobs
            title = job.find("h3").text.strip()
            company = job.find("h4").text.strip()
            link = job.find("a")["href"]
            job_list.append({"title": title, "company": company, "link": link})
    except Exception as e:
        print(f"Error fetching LinkedIn jobs: {e}")

    return job_list


# Function to search jobs on Glassdoor using Selenium
def search_jobs_on_glassdoor(query):
    job_list = []

    try:
        # Set up Selenium WebDriver
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run in headless mode
        driver = webdriver.Chrome(service=service, options=options)

        driver.get("https://www.glassdoor.com/Job/jobs.htm")

        time.sleep(3)
        search_box = driver.find_element(By.NAME, "sc.keyword")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        jobs = soup.find_all("li", class_="react-job-listing")

        for job in jobs[:50]:  # Limit to top 50 jobs
            title_tag = job.find("a", class_="jobLink")
            if title_tag:
                title = title_tag.text.strip()
                link = "https://www.glassdoor.com" + title_tag["href"]
                job_list.append({"title": title, "link": link})

    except Exception as e:
        print(f"Error fetching Glassdoor jobs: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()

    return job_list


# Function to save job listings to a JSON file
def save_jobs_to_json(jobs, filename="job_listings.json"):
    try:
        with open(filename, "w") as file:
            json.dump(jobs, file, indent=4)
        print(f"Job listings saved to {filename}")
    except Exception as e:
        print(f"Error saving jobs to JSON: {e}")


# Main function
def main():
    # Hardcoded PDF file path
    resume_path = "/Users/rejenthompson/Desktop/projects_cyber/SNUHacks/resume/job_opening/resume_Rejen.pdf"

    if not os.path.exists(resume_path):
        print("File not found! Please check the file path.")
        return

    if resume_path.endswith(".pdf"):
        resume_text = extract_text_from_pdf(resume_path)
    elif resume_path.endswith(".docx"):
        resume_text = extract_text_from_docx(resume_path)
    else:
        print("Unsupported file format! Please use a PDF or DOCX file.")
        return

    skills = extract_skills(resume_text)

    if not skills:
        print("No relevant skills found in the resume.")
        return

    print("\nExtracted Skills:", ", ".join(skills))

    query = " ".join(skills[:3])  # Use top 3 extracted skills for job search
    print(f"\nSearching jobs for: {query}")

    print("\nFetching LinkedIn job listings...")
    linkedin_jobs = search_jobs_on_linkedin(query)

    print("\nFetching Glassdoor job listings...")
    glassdoor_jobs = search_jobs_on_glassdoor(query)

    # Combine job listings
    all_jobs = linkedin_jobs + glassdoor_jobs

    # Save job listings to a JSON file
    save_jobs_to_json(all_jobs)


if __name__ == "__main__":
    main()