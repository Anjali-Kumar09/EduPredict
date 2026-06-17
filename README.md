# 🎓 EduPredict – Student Performance Prediction System

EduPredict is a comprehensive academic management and student performance analytics platform designed to help educational institutions make data-driven decisions. The system combines traditional academic management features with machine learning to identify students who may need additional support and predict future academic performance.

Built using Django and modern web technologies, EduPredict provides dedicated dashboards for administrators, teachers, and students, enabling seamless management of courses, assignments, grades, and academic records. The platform not only streamlines day-to-day academic operations but also offers valuable insights through interactive analytics, automated reporting, and performance prediction models.

The core objective of EduPredict is to assist educators in detecting potential academic risks early, allowing timely intervention and improving overall student success rates. By leveraging attendance records, assignment submissions, and academic performance data, the system generates meaningful predictions and personalized recommendations for students.

## ✨ Key Features

### 👥 Role-Based Access Control

* **Administrator Dashboard** – Manage users, departments, courses, and monitor institution-wide analytics.
* **Teacher Dashboard** – Create and manage courses, upload assignments, evaluate submissions, generate reports, and identify at-risk students.
* **Student Dashboard** – Enroll in courses, submit assignments, track grades, and receive personalized academic insights.

### 📊 Analytics & Reporting

* Interactive dashboards with performance visualizations.
* Student risk distribution and semester-wise performance analytics.
* Downloadable PDF performance reports.
* Excel export functionality for academic records and class reports.

### 🤖 Machine Learning Integration

* Predict student CGPA using a trained Random Forest Regression model.
* Risk classification based on predicted performance.
* Confidence scoring for prediction results.
* Batch prediction support through CSV uploads.
* Real-time calculation of attendance percentage and assignment submission rates.

### 🔐 Security & User Experience

* Custom authentication system with multiple user roles.
* Secure password reset functionality.
* Responsive and user-friendly interface built with Bootstrap 5.
* Modern dashboard design optimized for desktop and mobile devices.

## 🛠️ Technology Stack

| Layer            | Technologies                                        |
| ---------------- | --------------------------------------------------- |
| Backend          | Python 3.12, Django 5                               |
| Frontend         | HTML5, CSS3, Bootstrap 5, JavaScript, Chart.js      |
| Database         | SQLite (Development), PostgreSQL (Production Ready) |
| Machine Learning | Scikit-learn (Random Forest Regressor)              |
| Reporting        | ReportLab, OpenPyXL                                 |
| Authentication   | Custom Django User Model                            |

## 🎯 Project Goal

The primary goal of EduPredict is to bridge the gap between academic data and actionable insights. Instead of identifying struggling students after final examinations, educators can proactively monitor performance trends, predict outcomes, and provide timely support that enhances student learning and success.
