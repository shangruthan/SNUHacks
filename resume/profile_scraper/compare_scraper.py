from linkedin_api import Linkedin
from find_role import main  # Import the main function from find_role.py
import time

# Initialize the API client
api = Linkedin('', '')  # Replace with your credentials

# # Get job role and company from find_role.py
# job_info = main()  # Call the main function to extract job info
# print("Job Info:", job_info)  # Debugging line

# role = job_info["role"]
# company = job_info["company"]
# print("Role:", role)  # Debugging line
# print("Company:", company)  # Debugging line

# Search for people with the specified job role at the specified company
people = api.search_people(
    keyword_title="SDE",
    keyword_company="standard chartered"
)

for person in people:
    print(f"Name: {person['name']}")
    print(f"Title: {person['jobtitle']}")
    print(f"Location: {person['location']}")
    print("---")

for person in people:
    # Get full profile data
    if person.get('public_id'):
        profile = api.get_profile(public_id=person['public_id'])

        # Get contact information
        contact_info = api.get_profile_contact_info(
            public_id=person['public_id']
        )

        print(f"Name: {profile['firstName']} {profile['lastName']}")
        print(f"Email: {contact_info.get('email_address')}")
        print("---")

# print("Raw API Response:", people)  # Debugging line

# # Process the results
# for person in people:
#     print(f"Name: {person['name']}")
#     print(f"Title: {person['jobtitle']}")
#     print(f"Location: {person['location']}")
#     print("---")

# # Add a delay to avoid rate limits
# time.sleep(5)

# # Example of another search using the same role and company
# people = api.search_people(
#     keywords=role,
#     network_depths=["F", "S"],  # First and second connections
#     current_company=[company],  # Use the company name
#     profile_languages=["en"],  # Filter by language
#     regions=["us:0", "gb:0"]  # US and UK
# )
# print("Raw API Response (Second Search):", people)  # Debugging line

# # Process the results
# for person in people:
#     print(f"Name: {person['name']}")
#     print(f"Title: {person['jobtitle']}")
#     print(f"Location: {person['location']}")
#     print("---")