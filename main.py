from flask import Flask, request, render_template, send_file
import os
import PyPDF2
import docx2txt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fpdf import FPDF
import tempfile

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Helper functions
def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_text_from_doc(file_path):
    return docx2txt.process(file_path)

def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_text(file_path):
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".doc"):
        return extract_text_from_doc(file_path)
    elif file_path.endswith(".txt"):
        return extract_text_from_txt(file_path)
    else:
        return ""

# Function to generate PDF report
def generate_pdf_report(top_resumes, similarity_scores, job_description):
    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt="Top Resume Matches", ln=True, align='C')

    # Job Description
    pdf.set_font('Arial', '', 12)
    pdf.cell(200, 10, txt="Job Description:", ln=True, align='L')
    pdf.multi_cell(0, 10, txt=job_description)

    # Resume Matching Summary
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(200, 10, txt="Top Matching Resumes:", ln=True, align='L')

    # Add each resume and similarity score
    for i, resume in enumerate(top_resumes):
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f"{i + 1}. {resume} (Similarity Score: {similarity_scores[i]})", ln=True)

    # Save PDF to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
        pdf.output(temp.name)
        return temp.name

@app.route("/")
def matchresume():
    return render_template('matchMyResume.html')

@app.route("/matcher", methods=['GET', 'POST'])
def matcher():
    if request.method == 'POST':
        job_description = request.form.get('job_description')
        resume_files = request.files.getlist('resumes')  # Handle file uploads

        resumes = []
        for resume_file in resume_files:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
            resume_file.save(filename)
            resumes.append(extract_text(filename))

        if not resumes or not job_description:
            return render_template('matchMyResume.html', message="You have to upload both the resume and job description to proceed further!")

        # TF-IDF Vectorization
        vectorizer = TfidfVectorizer().fit_transform([job_description] + resumes)
        vectors = vectorizer.toarray()
        job_vector = vectors[0]
        resume_vectors = vectors[1:]
        similarities = cosine_similarity([job_vector], resume_vectors)[0]

        # Get top 3 matching resumes
        top_indices = similarities.argsort()[-3:][::-1]
        top_resumes = [resume_files[i].filename for i in top_indices]
        similarity_scores = [round(similarities[i], 2) for i in top_indices]

        # Generate PDF report for download
        if 'download_report' in request.form:
            pdf_file_path = generate_pdf_report(top_resumes, similarity_scores, job_description)
            return send_file(pdf_file_path, as_attachment=True, download_name="resume_match_report.pdf")

        # Display summary of top 3 resumes with skills
        top_resume_summaries = [f"Resume: {resume_files[i].filename}, Skills Matched: (Sample Skills)" for i in top_indices]

        return render_template('matchMyResume.html', message="Top matching resumes:", top_resumes=top_resumes, similarity_scores=similarity_scores, resume_summaries=top_resume_summaries)

    return render_template('matchMyResume.html')

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
