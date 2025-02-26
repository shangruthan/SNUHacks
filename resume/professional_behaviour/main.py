from datetime import datetime
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np

# Import the dictionary from the .py file
from linkedin_data import linkedin_data

# Function to parse date strings into datetime objects
def parse_date(year, month=None):
    return datetime(year=year, month=month if month else 1, day=1)

# 1. Basic Information
print("Candidate Name:", linkedin_data.get("firstName"), linkedin_data.get("lastName"))
print("Headline:", linkedin_data.get("headline"))

# 2. Employment Gaps
print("\nProfessional Behavior Analysis:")

experience = linkedin_data.get("experience", [])
if len(experience) > 1:
    gaps = []
    for i in range(1, len(experience)):
        # Handle missing endDate for the previous job
        prev_end_date = experience[i - 1]["timePeriod"].get("endDate")
        if prev_end_date:
            prev_end = parse_date(prev_end_date["year"], prev_end_date.get("month"))
        else:
            prev_end = datetime.now()  # Assume the previous job is ongoing

        # Handle missing startDate for the current job
        curr_start_date = experience[i]["timePeriod"].get("startDate")
        if curr_start_date:
            curr_start = parse_date(curr_start_date["year"], curr_start_date.get("month"))
        else:
            continue  # Skip if startDate is missing

        gap = (curr_start - prev_end).days / 30  # Convert gap to months
        if gap > 0:
            gaps.append({
                "previous_role": experience[i - 1]["title"],
                "next_role": experience[i]["title"],
                "gap_months": round(gap, 1)
            })
    print("\n1. Employment Gaps:")
    for gap in gaps:
        print(f"- Between {gap['previous_role']} and {gap['next_role']}: {gap['gap_months']} months")
else:
    print("\n1. Employment Gaps: No gaps found.")

# 3. Career Progression
roles = [exp["title"] for exp in experience]
print("\n2. Career Progression:")
print(" → ".join(roles))

# 4. Skill Development
skills = linkedin_data.get("skills", [])
print("\n3. Skill Development:")
print(f"- Total Skills: {len(skills)}")
print(f"- Skills: {', '.join([skill['name'] for skill in skills])}" if skills else "- No skills listed.")

# 5. Job Stability
tenures = []
for exp in experience:
    start_date = exp["timePeriod"].get("startDate")
    if start_date:
        start = parse_date(start_date["year"], start_date.get("month"))
    else:
        continue  # Skip if startDate is missing

    end_date = exp["timePeriod"].get("endDate")
    if end_date:
        end = parse_date(end_date["year"], end_date.get("month"))
    else:
        end = datetime.now()  # Assume the job is ongoing

    tenure = (end - start).days / 365  # Convert tenure to years
    tenures.append(tenure)
avg_tenure = round(sum(tenures) / len(tenures), 2) if tenures else 0
print("\n4. Job Stability:")
print(f"- Average Tenure: {avg_tenure} years per job")

# 6. Industry Trends
industries = set()
for exp in experience:
    if "industries" in exp.get("company", {}):
        industries.update(exp["company"]["industries"])
print("\n5. Industry Trends:")
print("- Worked in industries:", ", ".join(industries) if industries else "N/A")

# 7. Education Relevance
education = linkedin_data.get("education", [])
education_relevance = "Relevant" if any("cyber" in edu.get("fieldOfStudy", "").lower() for edu in education) else "Not Relevant"
print("\n6. Education Relevance:")
print(f"- {education_relevance}")

# 8. Social Proof
recommendations = len(linkedin_data.get("recommendations", []))
print("\n7. Social Proof:")
print(f"- Recommendations: {recommendations}")

# 9. NLP and Clustering Insights
job_descriptions = [exp.get("description", "") for exp in experience]
if any(job_descriptions):
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(job_descriptions)
    num_clusters = min(2, len(job_descriptions))  # Adjust based on data
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(tfidf_matrix)
    clusters = kmeans.labels_

    cluster_groups = defaultdict(list)
    for i, exp in enumerate(experience):
        cluster_groups[clusters[i]].append(exp["title"])

    print("\n8. NLP and Clustering Insights:")
    for cluster, roles in cluster_groups.items():
        print(f"- Cluster {cluster}: Roles {', '.join(roles)}")
        print(f"  Themes: {vectorizer.get_feature_names_out()[np.argsort(kmeans.cluster_centers_[cluster])[-5:]]}")  # Top 5 themes
else:
    print("\n8. NLP and Clustering Insights: No job descriptions available.")

# 10. Summary Analysis (NLP)
summary = linkedin_data.get("summary", "")
if summary:
    print("\n9. Summary Analysis:")
    print("- Key Themes:", ", ".join(set(summary.lower().split()[:10])))  # Extract top 10 words
else:
    print("\n9. Summary Analysis: No summary available.")