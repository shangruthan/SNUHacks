# README: Applicant Tracking System (ATS) and Resume Enhancement Tool

---

Welcome to the **Applicant Tracking System (ATS) and Resume Enhancement Tool**! This project is a dual-purpose solution designed to cater to **recruiters** and **students/job seekers**. It leverages AI-powered analysis, skill gap identification, resume enhancement, and portfolio generation to streamline the hiring process and improve job application outcomes.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Features Overview](#features-overview)
3. [Candidate Features (Students/Job Seekers)](#candidate-features-studentsjob-seekers)
4. [Recruiter Features](#recruiter-features)
5. [Flowchart](#flowchart)
6. [Tech Stack](#tech-stack)
7. [How to Use](#how-to-use)
8. [Future Enhancements](#future-enhancements)

---

## Introduction

The ATS and Resume Enhancement Tool is an AI-powered platform that bridges the gap between recruiters and job seekers by:

- Helping recruiters evaluate candidates efficiently.
- Empowering candidates to create ATS-compliant resumes and identify skill gaps.

This tool uses **Natural Language Processing (NLP)** via the Groq API, data visualization with Matplotlib, and a robust backend built with Flask and SQLite.

---

## Features Overview

### For Candidates (Students/Job Seekers):

- **Resume Enhancer**: Upload resumes to receive ATS-compliant suggestions for improvement.
- **Skill Gap Analyzer**: Compare resumes against job descriptions and get recommendations for missing skills.
- **LinkedIn Scraper**: Extract data from LinkedIn profiles to structure resumes.
- **Portfolio Generator**: Create a simple portfolio website from resume data.


### For Recruiters:

- **Resume Evaluator**: Parse resumes, extract relevant information, and score candidates based on custom weightage.
- **Ranking System**: Match candidates to job requirements and rank them based on relevance.
- **Analytics Dashboard**: Visualize hiring trends, candidate rankings, and statistics.

---

## Candidate Features (Students/Job Seekers)

### 1. Resume Enhancer

- Upload your resume in PDF/DOCX format.
- The system parses your resume data and formats it for ATS compliance.
- It optimizes sections like work experience, skills, education, etc., based on job descriptions.
- Outputs an enhanced resume ready for download.


### 2. Skill Gap Analyzer

- Upload your resume and input a job description.
- The system extracts key skills from the job description using NLP.
- Compares your resume against the job description to identify missing skills or qualifications.
- Provides actionable suggestions such as online courses or certifications to bridge these gaps.


### 3. LinkedIn Scraper

- Input your LinkedIn profile URL.
- The scraper extracts educational qualifications, skills, and work experience from your profile.
- Converts the data into JSON format for further processing.
- Generates an ATS-compliant resume based on this data.


### 4. Portfolio Maker

- Upload your enhanced resume.
- Parses the data to generate a simple portfolio website showcasing your education, skills, projects, and work experience.
- Allows downloading or hosting of the portfolio.

---

## Recruiter Features

### 1. Resume Evaluator

- Set custom weights for work experience, skills, education, etc., based on job requirements.
- Parse uploaded resumes to extract relevant information using NLP techniques.
- Apply scoring algorithms to generate candidate scores based on relevance.


### 2. Ranking System

- Extract job requirements from descriptions provided by recruiters.
- Match candidates' resumes against these requirements using advanced algorithms.
- Rank candidates dynamically based on scores rather than filtering out profiles entirely.
- Handle edge cases like low CGPA or missing skills by re-ranking based on dynamic criteria.


### 3. Analytics Dashboard

- Collect data from evaluated resumes and rankings.
- Visualize insights through charts and graphs using Matplotlib.
    - Examples: Hiring trends, candidate performance comparisons, etc.
- Allow recruiters to adjust parameters dynamically for better decision-making.

---

## Flowchart

The attached flowchart provides a detailed representation of the solution's workflow for both **candidates** and **recruiters**, highlighting key features like resume enhancement, skill gap analysis, ranking systems, portfolio generation, and analytics dashboards.
![Flow chart](https://github.com/user-attachments/assets/0f01f2ab-d8a0-4346-9df2-965962458206)

---

## Tech Stack

1. **Backend**: Python (Flask framework)
2. **Frontend**: HTML, CSS (custom styles), JavaScript
3. **Database**: SQLite
4. **AI/NLP**: Groq API for natural language processing![Uploading Flow chart.png…]()

5. **Data Visualization**: Matplotlib for analytics graphs
6. **File Handling**: Secure upload of PDF/DOCX files

---

## How to Use

### For Candidates:

1. Navigate to the "Candidate" section in the web interface.
2. Choose one of the available tools:
    - Upload your resume for enhancement or skill gap analysis.
    - Input a LinkedIn profile URL for scraping data into a structured format.
    - Generate a portfolio website using parsed resume data.
3. Download the enhanced resume or portfolio once processing is complete.

### For Recruiters:

1. Login as a recruiter through the web interface.
2. Use the "Resume Evaluator" feature to upload candidate resumes and set custom weightage for evaluation criteria.
3. View ranked candidates in the "Ranking System" section based on relevance scores.
4. Access detailed insights in the "Analytics Dashboard" section with visualized hiring trends and statistics.

---

## Future Enhancements

1. **Machine Learning Integration**:
    - Train models for more accurate candidate ranking and predictive analytics.
2. **Scalability Improvements**:
    - Upgrade SQLite database to a more scalable option like PostgreSQL for larger datasets.
3. **Real-Time Collaboration Tools**:
    - Add real-time chat support between recruiters and candidates.
4. **Mobile Application Development**:
    - Extend functionality to mobile platforms for better accessibility.
5. **Integration with Job Portals**:
    - Directly connect with platforms like LinkedIn or Indeed for real-time job postings.
  
  

---

This README provides a comprehensive overview of the project’s features, workflow, tech stack, and usage instructions for both students/job seekers and recruiters!





