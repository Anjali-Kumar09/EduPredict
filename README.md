# 🎓 EduPredict – Student Performance Prediction System

[![Django Version](https://img.shields.io/badge/Django-5.0.6-green)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)

**EduPredict** is a full‑stack web application that helps colleges predict student performance using machine learning.  
It gives teachers an early‑warning system and lets students see their predicted CGPA – all in one clean, role‑based platform.

---

## ✨ What the system can do

- **Three roles** – Admin, Teacher, Student (each with their own dashboard)
- **Course & assignment management** – teachers create assignments, students submit work, teachers grade online
- **Smart reports** – generate PDF student reports and export class performance to Excel
- **Live analytics** – risk distribution pie chart, students‑by‑semester bar chart (admin only)
- **AI‑powered CGPA prediction** – uses a Random Forest model to predict future CGPA based on:
  - Previous CGPA
  - Real attendance % (last 30 days)
  - Assignment submission rate
  - Study hours, backlogs, family income, high school %, entrance score
- **Batch prediction** – upload a CSV file with student data, get back a CSV with predicted CGPA for every row
- **Clean, responsive design** – cream colour theme, works on desktop and mobile

---

## 🤖 Machine Learning – How it works (no math, just the idea)

We trained a **Random Forest Regressor** on 2000 synthetic student records.  
The model learns which features (attendance, previous marks, study hours, etc.) matter most for final CGPA.

- **Single prediction** – teacher picks a student from a dropdown, clicks “Predict CGPA”, and instantly sees predicted CGPA, risk level (Low/Medium/High), and confidence score.
- **Batch prediction** – teacher uploads a CSV containing the 8 input features, the system processes every row and returns a new CSV with an extra `predicted_cgpa` column.

Confidence may be low when there aren’t enough real attendance/submission records – that’s normal. With more data, confidence rises.

---

## 🛠️ Tech stack (what I used)

| Layer | Technology |
|-------|------------|
| Backend | Python 3.12, Django 5.0 |
| Frontend | HTML,Css, Bootstrap 5, Chart.js, Font Awesome |
| Database | SQLite (development) / PostgreSQL (production ready) |
| Machine Learning | scikit‑learn (Random Forest), pandas, numpy, joblib |
| Reports | ReportLab (PDF), openpyxl (Excel) |

---

## How to run the project (for someone who clones it)

```bash
git clone https://github.com/Anjali-Kumar09/EduPredict.git
cd EduPredict
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver