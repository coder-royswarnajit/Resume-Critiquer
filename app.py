import streamlit as st
import groq
import PyPDF2
import io
import os
import pandas as pd
from dotenv import load_dotenv
from job_search import JobSearcher

load_dotenv()

st.set_page_config(page_title='Agragrati - AI Resume & Job Search',layout='wide')

st.title('🎯 Agragrati - AI Resume & Job Search')
st.markdown('Upload your resume to receive feedback and find real job opportunities!')

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize job searcher
if GROQ_API_KEY:
    job_searcher = JobSearcher(GROQ_API_KEY)
else:
    st.error("GROQ_API_KEY not found. Please check your .env file.")
    st.stop()

# Create tabs for different functionalities
tab1, tab2, tab3 = st.tabs(["📄 Resume Analysis", "🔍 Job Search", "💡 Career Insights"])

with tab1:
    st.header("Resume Analysis")
    uploaded_file = st.file_uploader("Upload Your Resume (PDF or TXT)", type=["pdf","txt"])
    job_role = st.text_input("Enter the job role you are targeting (optional)")
    analyze = st.button("Analyze Resume", type="primary")

with tab2:
    st.header("Job Search")

    # Show API status
    api_status = []
    if job_searcher.rapidapi_key and job_searcher.rapidapi_key != "your_rapidapi_key_here":
        api_status.append("✅ JSearch API")
    else:
        api_status.append("❌ JSearch API (not configured)")

    if (job_searcher.adzuna_app_id and job_searcher.adzuna_app_id != "your_adzuna_app_id_here" and
        job_searcher.adzuna_app_key and job_searcher.adzuna_app_key != "your_adzuna_app_key_here"):
        api_status.append("✅ Adzuna API")
    else:
        api_status.append("❌ Adzuna API (not configured)")

    st.info(f"**API Status**: {' | '.join(api_status)}")

    if not any("✅" in status for status in api_status):
        st.warning("⚠️ No job search APIs configured. Will show sample data. See README for API setup instructions.")

    # Job search options
    search_option = st.radio(
        "Choose search method:",
        ["🤖 Smart Search (Based on Resume)", "✍️ Manual Search"]
    )

    col1, col2 = st.columns(2)

    with col1:
        if search_option == "✍️ Manual Search":
            search_term = st.text_input("Job title or keywords", placeholder="e.g., Software Engineer, Data Analyst")
        else:
            search_term = None
            st.info("Upload your resume in the Resume Analysis tab first, then return here for smart job search.")

        location = st.text_input("Location", value="United States", placeholder="e.g., San Francisco, CA")

    with col2:
        job_type_filter = st.selectbox(
            "Job Type",
            ["Any", "Full-time", "Part-time", "Contract", "Internship"]
        )

        results_count = st.slider("Number of results", min_value=10, max_value=50, value=20)

    search_jobs = st.button("🔍 Search Jobs", type="primary")

with tab3:
    st.header("Career Insights")
    st.info("Upload your resume and analyze it to get personalized career recommendations!")

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

# Store resume content in session state for use across tabs
if 'resume_content' not in st.session_state:
    st.session_state.resume_content = None
if 'resume_analyzed' not in st.session_state:
    st.session_state.resume_analyzed = False

# Resume Analysis Logic
if analyze and uploaded_file:
    with tab1:
        file_content = extract_text_from_file(uploaded_file)

        if not file_content.strip():
            st.error("File does not have any content!!")
            st.stop()

        # Store resume content in session state
        st.session_state.resume_content = file_content
        st.session_state.resume_analyzed = True

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
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "You are an expert resume reviewer with years of experience in HR and recruitment."},
                      {"role": "user", "content": prompt}],
            temperature=0.7,
        )

        st.balloons()

        st.markdown('### 📋 Resume Analysis Results:')
        st.markdown(response.choices[0].message.content)

        # Show career insights in tab3
        with tab3:
            st.success("✅ Resume analyzed! Here are your personalized career insights:")

            # Get job recommendations
            recommendations = job_searcher.get_job_recommendations(file_content, job_role)

            if recommendations:
                st.markdown("### 🎯 Job Search Recommendations:")
                for i, rec in enumerate(recommendations, 1):
                    st.markdown(f"{i}. {rec}")

            # Extract skills for display
            skills = job_searcher.extract_skills_from_resume(file_content)
            if skills:
                st.markdown("### 🔧 Key Skills Identified:")
                # Display skills as tags
                skills_html = " ".join([f'<span style="background-color: #e1f5fe; padding: 4px 8px; margin: 2px; border-radius: 12px; font-size: 12px;">{skill}</span>' for skill in skills])
                st.markdown(skills_html, unsafe_allow_html=True)

# Job Search Logic
if search_jobs:
    with tab2:
        if search_option == "🤖 Smart Search (Based on Resume)":
            if not st.session_state.resume_content:
                st.error("Please upload and analyze your resume first in the Resume Analysis tab.")
            else:
                st.info("Searching for jobs based on your resume...")
                job_type_param = None if job_type_filter == "Any" else job_type_filter
                jobs_df = job_searcher.search_jobs_by_resume(
                    st.session_state.resume_content,
                    location,
                    results_count,
                    job_type_param
                )

                if not jobs_df.empty:
                    st.success(f"Found {len(jobs_df)} job opportunities!")

                    # Display job results
                    st.markdown("### 💼 Job Search Results:")

                    # Add filters for the results
                    col1, col2 = st.columns(2)
                    with col1:
                        if 'Company' in jobs_df.columns:
                            companies = ['All'] + sorted(jobs_df['Company'].dropna().unique().tolist())
                            selected_company = st.selectbox("Filter by Company", companies)

                    with col2:
                        if 'Source' in jobs_df.columns:
                            sources = ['All'] + sorted(jobs_df['Source'].dropna().unique().tolist())
                            selected_source = st.selectbox("Filter by Source", sources)

                    # Apply filters
                    filtered_df = jobs_df.copy()
                    if selected_company != 'All' and 'Company' in jobs_df.columns:
                        filtered_df = filtered_df[filtered_df['Company'] == selected_company]
                    if selected_source != 'All' and 'Source' in jobs_df.columns:
                        filtered_df = filtered_df[filtered_df['Source'] == selected_source]

                    # Display filtered results
                    st.dataframe(
                        filtered_df,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "Apply Link": st.column_config.LinkColumn("Apply Link")
                        }
                    )

                    # Download option
                    csv = filtered_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Results as CSV",
                        data=csv,
                        file_name="job_search_results.csv",
                        mime="text/csv"
                    )

        else:  # Manual search
            if not search_term:
                st.error("Please enter a job title or keywords to search.")
            else:
                st.info(f"Searching for '{search_term}' jobs...")
                job_type_param = None if job_type_filter == "Any" else job_type_filter
                jobs_df = job_searcher.search_jobs(
                    search_term,
                    location,
                    results_count,
                    job_type_param
                )

                if not jobs_df.empty:
                    st.success(f"Found {len(jobs_df)} job opportunities!")

                    # Display job results (same as above)
                    st.markdown("### 💼 Job Search Results:")

                    # Add filters for the results
                    col1, col2 = st.columns(2)
                    with col1:
                        if 'Company' in jobs_df.columns:
                            companies = ['All'] + sorted(jobs_df['Company'].dropna().unique().tolist())
                            selected_company = st.selectbox("Filter by Company", companies, key="manual_company")

                    with col2:
                        if 'Source' in jobs_df.columns:
                            sources = ['All'] + sorted(jobs_df['Source'].dropna().unique().tolist())
                            selected_source = st.selectbox("Filter by Source", sources, key="manual_source")

                    # Apply filters
                    filtered_df = jobs_df.copy()
                    if selected_company != 'All' and 'Company' in jobs_df.columns:
                        filtered_df = filtered_df[filtered_df['Company'] == selected_company]
                    if selected_source != 'All' and 'Source' in jobs_df.columns:
                        filtered_df = filtered_df[filtered_df['Source'] == selected_source]

                    # Display filtered results
                    st.dataframe(
                        filtered_df,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "Apply Link": st.column_config.LinkColumn("Apply Link")
                        }
                    )

                    # Download option
                    csv = filtered_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Results as CSV",
                        data=csv,
                        file_name="job_search_results.csv",
                        mime="text/csv",
                        key="manual_download"
                    )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <h4>🎯 Agragrati - AI Resume & Job Search</h4>
    <p>Get AI-powered resume feedback and find real job opportunities!</p>
    <p><strong>Features:</strong> Resume Analysis • Smart Job Search • Career Insights</p>
    <p><em>Powered by Groq AI & Real Job APIs</em></p>
</div>
""", unsafe_allow_html=True)