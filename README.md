# 🎓 EduPredict – Student Performance Prediction System

[![Django Version](https://img.shields.io/badge/Django-5.0.6-green)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)

A full‑stack web application that helps educational institutions predict student performance, manage assignments, and generate insightful reports – all through a single, role‑based platform.

## ✨ Features

### 👥 Role‑Based Dashboards
- **Admin** – full control over users, courses, departments, and system analytics.
- **Teacher** – create courses, upload assignments, view submissions, grade, export Excel reports, and identify at‑risk students.
- **Student** – enrol in courses, submit assignments, view grades and personalised recommendations.

### 📊 Analytics & Reporting
- **Admin analytics** – risk distribution pie chart, students‑per‑semester bar chart.
- **PDF reports** – downloadable student performance summaries (ReportLab).
- **Excel exports** – class performance sheets (openpyxl).

### 🔐 Security & Usability
- Custom user model with roles (Admin, Teacher, Student, Parent).
- Password reset via email (console backend for development).
- Responsive cream‑themed UI (Bootstrap 5, Font Awesome, Chart.js).

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.12, Django 5.0 |
| Frontend | Bootstrap 5, Chart.js, Font Awesome |
| Database | SQLite (dev), PostgreSQL (production ready) |
| ML | scikit‑learn (Random Forest – ready to integrate) |
| Reporting | ReportLab (PDF), openpyxl (Excel) |

## 📦 Installation (Local)

1. **Clone the repository**
   ```bash
   git clone https://github.com/Anjali-Kumar09/EduPredict.git
   cd EduPredict