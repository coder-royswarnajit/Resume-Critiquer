import streamlit as st
import groq
import PyPDF2
import io
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title='Resume Critiquer',layout='centered')

st.title('Resume Critiquer')
st.markdown('Upload your resume in PDF format to receive feedback.')

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

uploaded_file=st.file_uploader("Upload Your Resume (PDF or TXT)", type=["pdf","txt"])
job_role=st.text_input("Enter the job role you are targetting (optional)")

analyze = st.button("Analyze")

def extract_text_pdf(file):
    pdf_reader=PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    
    return text

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")


if analyze and uploaded_file:
    file_content = extract_text_from_file(uploaded_file)
    
    if not file_content.strip():
        st.error("File does have any content!!")
        st.stop()
        
    prompt = f"""
    You are an expert resume reviewer and career consultant with 15+ years of experience in talent acquisition and HR. 
    Analyze the following resume and provide comprehensive, actionable feedback for {job_role if job_role else 'general job applications'}.

    **ANALYSIS FRAMEWORK:**
    Please structure your response with the following sections:

    1. **OVERALL IMPRESSION** (1-2 sentences)
    - First impression and general quality assessment

    2. **STRENGTHS** 
    - What works well in this resume
    - Standout achievements or experiences

    3. **AREAS FOR IMPROVEMENT**
    - Content gaps or weaknesses
    - Formatting and presentation issues
    - Missing key information

    4. **SPECIFIC RECOMMENDATIONS**
    - Concrete suggestions for improvement
    - Industry-specific advice for {job_role if job_role else 'General Job Applications'}
    - Keywords and skills to consider adding

    5. **ACTION ITEMS** 
    - Priority fixes (High/Medium/Low)
    - Quick wins that can be implemented immediately

    6. **FINAL SCORE** 
    - Rate the resume from 1-10 with brief justification

    **RESUME CONTENT:**
    {file_content}

    **INSTRUCTIONS:**
    - Be honest but constructive in your feedback
    - Provide specific examples from the resume when pointing out issues
    - Consider ATS (Applicant Tracking System) compatibility
    - Focus on relevance to {job_role if job_role else 'modern job market standards'}
    - Suggest specific metrics, action verbs, and formatting improvements
    - Keep feedback actionable and prioritized
    """
    
    client = groq.Client(api_key=GROQ_API_KEY)
    response=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": "You are an expert resume reviewer with years of experience in HR and recruitment."},
                  {"role": "user", "content": prompt}],
        temperature=0.7,
        
    )

    st.balloons()
    
    st.markdown('### Feedback:')
    st.markdown(response.choices[0].message.content)