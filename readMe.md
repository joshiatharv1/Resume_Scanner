# 💼 MatchMyResume – Resume Matcher Web App

## 🔍 Overview
**MatchMyResume** is a web-based application that matches resumes to a given job description using text similarity techniques from Natural Language Processing (NLP). It helps recruiters or hiring managers identify the most relevant candidates by ranking uploaded resumes based on how closely they align with the job requirements.

---

## ⚙️ Features
- Upload multiple resumes in `.pdf`, `.docx`, or `.txt` format
- Enter a job description for comparison
- Automatic text extraction from resumes
- Text similarity scoring using **TF-IDF** and **cosine similarity**
- Displays top 3 resume matches
- Option to download a detailed PDF report

---

## 🧠 Machine Learning Concept Used

This project uses **unsupervised machine learning** to perform text similarity matching.

### 🔸 Techniques Involved:
- **TF-IDF (Term Frequency-Inverse Document Frequency)**  
  Converts the text content of resumes and job description into numerical vectors based on word relevance.

- **Cosine Similarity**  
  Measures the angle (similarity) between vectors to identify how closely each resume matches the job description.

> No labeled data is used; this is a pure similarity-based approach without model training.

---

## 💻 Technologies Used

### 🔹 Frontend:
- HTML5 + CSS3
- [Bootstrap 4](https://getbootstrap.com/)
- Jinja2 Templating (Flask integration)

### 🔹 Backend:
- **Flask** (Python web framework)
- `PyPDF2`, `docx2txt` – for file parsing
- `scikit-learn` – for TF-IDF and cosine similarity
- `FPDF` – for generating downloadable PDF reports

---

## 🗂️ Folder Structure

