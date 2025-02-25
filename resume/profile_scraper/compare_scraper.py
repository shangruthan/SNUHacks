from linkedin_api import Linkedin
from find_role import main  # Import the main function from main.py

# Initialize the API client
api = Linkedin('shangrutha@gmail.com', '-Ye:yYwf93Aq49h')  # Replace with your credentials

# Get job role and company from main.py
job_info = main()  # Call the main function to extract job info
role = job_info["role"]
company = job_info["company"]

# Search for people with the specified job role at the specified company
people = api.search_people(
    keyword_title=role,
    keyword_company=company
)

# Process the results
for person in people:
    print(f"Name: {person['name']}")
    print(f"Title: {person['jobtitle']}")
    print(f"Location: {person['location']}")
    print("---")

# Example of another search using the same role and company
people = api.search_people(
    keywords=role,
    network_depths=["F", "S"],  # First and second connections
    current_company=[company],  # Use the company name
    profile_languages=["en"],  # Filter by language
    regions=["us:0", "gb:0"]  # US and UK
)

# Process the results
for person in people:
    print(f"Name: {person['name']}")
    print(f"Title: {person['jobtitle']}")
    print(f"Location: {person['location']}")
    print("---")