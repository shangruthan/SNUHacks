import os
import time
import json
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# Load credentials from .env file
load_dotenv()
LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

# List of LinkedIn profiles to scrape
LINKEDIN_PROFILES = [
    "https://www.linkedin.com/in/suwaidaslam/"
]

def setup_driver():
    """Set up Selenium WebDriver with Chromium"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (No GUI)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    return driver

def login(driver):
    """Log in to LinkedIn using credentials"""
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)

    driver.find_element(By.ID, "username").send_keys(LINKEDIN_EMAIL)
    driver.find_element(By.ID, "password").send_keys(LINKEDIN_PASSWORD)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    
    time.sleep(5)  # Wait for login to complete

def scroll_down(driver):
    """Scroll down slowly to load all dynamic content"""
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for new elements to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def scrape_profile(driver, profile_url):
    """Scrape LinkedIn profile data"""
    driver.get(profile_url)
    time.sleep(3)  # Let page load
    scroll_down(driver)  # Load all content dynamically

    src = driver.page_source
    soup = BeautifulSoup(src, "html.parser")

    def extract_text(selector, attribute=None):
        """Helper function to extract text safely"""
        try:
            element = soup.select_one(selector)
            return element[attribute] if attribute else element.get_text(strip=True)
        except:
            return "Not found"

    profile_data = {
        "Name": extract_text("h1.text-heading-xlarge"),
        "Headline": extract_text("div.text-body-medium.break-words"),
        "Location": extract_text("span.text-body-small.inline.t-black--light"),
        "About": extract_text("section.summary p"),
        "Current Experience": extract_text("section.experience div.current"),
        "Past Experience": extract_text("section.experience div.previous"),
        "Education": extract_text("section.education"),
        "Skills": extract_text("section.skills"),
        "Contact Info": []
    }

    # Extract contact info
    contact_url = profile_url + "detail/contact-info/"
    driver.get(contact_url)
    time.sleep(2)
    contact_soup = BeautifulSoup(driver.page_source, "html.parser")

    try:
        contact_section = contact_soup.select_one("section.pv-contact-info")
        if contact_section:
            for a in contact_section.find_all("a", href=True):
                profile_data["Contact Info"].append(a["href"])
    except:
        profile_data["Contact Info"].append("Not found")

    return profile_data

if __name__ == "__main__":
    driver = setup_driver()
    try:
        login(driver)

        all_profiles_data = []
        for profile in LINKEDIN_PROFILES:
            print(f"🔍 Scraping profile: {profile}")
            data = scrape_profile(driver, profile)
            all_profiles_data.append(data)

        # Save results to JSON
        with open("linkedin_profiles.json", "w", encoding="utf-8") as json_file:
            json.dump(all_profiles_data, json_file, indent=4, ensure_ascii=False)

        # Save results to CSV
        df = pd.DataFrame(all_profiles_data)
        df.to_csv("linkedin_profiles.csv", index=False)

        print("✅ Scraping completed! Data saved to linkedin_profiles.json and linkedin_profiles.csv")

    finally:
        driver.quit()
