import json
from linkedin_scraper import Person, actions
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

# Set up Edge options (if needed)
options = Options()
options.add_argument('--start-maximized')  # Example option to start maximized

# Path to Edge WebDriver (msedgedriver.exe) in your folder
service = Service(executable_path='C:/Users/shang/Downloads/edgedriver_win64/msedgedriver.exe')

# Initialize the Edge WebDriver
driver = webdriver.Edge(service=service, options=options)

try:
    # Log into LinkedIn (replace 'your_username' and 'your_password' with actual credentials)
    actions.login(driver, "thisisnk3794@gmail.com", "nareshkumar")  # Enter your LinkedIn credentials

    # Scrape a LinkedIn profile
    profile_url = "https://www.linkedin.com/in/rejen-thompson-765271258"  # Example profile URL
    person = Person(profile_url, driver=driver, scrape=True)

    # Extract profile data
    profile_data = {
        "Name": person.name,
        "Job Title": person.job_title,
        "Company": person.company,
        "Education": [{
            "Institution": edu.institution_name if hasattr(edu, 'institution_name') else None,
            "Degree": edu.degree if hasattr(edu, 'degree') else None,
            "Field of Study": edu.field_of_study if hasattr(edu, 'field_of_study') else None,
            "Dates": edu.dates if hasattr(edu, 'dates') else None
        } for edu in person.educations] if hasattr(person, 'educations') else [],
        "Skills": person.skills if hasattr(person, 'skills') else [],
        "Experiences": [{
            "Title": exp.position_title if hasattr(exp, 'position_title') else None,
            "Company": exp.institution_name if hasattr(exp, 'institution_name') else None,
            "Dates": exp.dates if hasattr(exp, 'dates') else None,
            "Location": exp.location if hasattr(exp, 'location') else None
        } for exp in person.experiences] if hasattr(person, 'experiences') else []
    }

    # Output to JSON and save to file
    with open('profile_data.json', 'w') as json_file:
        json.dump(profile_data, json_file, indent=4)

    print("Profile data saved to profile_data.json")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the Edge driver
    driver.quit()