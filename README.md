# Resume Critiquer 📄

An AI-powered resume analysis tool built with Streamlit and Groq AI that provides comprehensive, structured feedback and improvement suggestions for job seekers---

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Ensure all prerequisites are met
3. Verify your API key is valid and active
4. Try restarting the application

---

## 🌟 Features Overview

### What Makes This Tool Special:

- **🎯 Targeted Analysis**: Provides job-specific recommendations
- **� Structured Output**: Organized feedback in 6 clear sections
- **⚡ Fast Processing**: Quick AI-powered analysis
- **🔒 Privacy Focused**: Your resume data is processed securely
- **💰 Cost Effective**: Uses free Groq API with generous limits
- **�🚀 Easy Deployment**: Multiple setup options for all skill levels

### Sample Analysis Output:

The tool provides feedback in these structured sections:
1. **Overall Impression** - Quick quality assessment
2. **Strengths** - What's working well
3. **Areas for Improvement** - Specific issues identified
4. **Recommendations** - Concrete improvement suggestions
5. **Action Items** - Prioritized tasks (High/Medium/Low)
6. **Final Score** - Numerical rating (1-10) with justification

Perfect for job seekers, career counselors, and HR professionals! 🎉

---

## 📄 License

This project is open source and available under the MIT License.Features

- **📁 Multi-Format Support**: Upload resumes in PDF or TXT format
- **🤖 AI-Powered Analysis**: Uses advanced Groq Llama models for intelligent feedback
- **📊 Structured Feedback**: Get organized analysis with scores and prioritized action items
- **🎯 Job-Specific Advice**: Tailored recommendations based on target job role
- **🔍 ATS Compatibility**: Checks for Applicant Tracking System optimization
- **⚡ Real-time Processing**: Fast analysis with detailed improvement suggestions

## 📋 Prerequisites

Before you can run this application, you need:

1. **Groq API Key** (Required)
   - Sign up at [console.groq.com](https://console.groq.com/keys)
   - Generate a free API key
   - Note: Free tier includes generous usage limits

2. **Choose Your Setup Method**:
   - **Option A**: Docker (Recommended - No Python setup needed)
   - **Option B**: Local Python Environment

---

## 🐳 Method A: Docker Deployment (Recommended)

### What You Need:
- Docker Desktop installed ([Download here](https://www.docker.com/products/docker-desktop/))
- Your Groq API key

### Step-by-Step Setup:

1. **Download/Clone this project** to your computer

2. **Create the API key file**:
   - Open the `.env` file in the project folder
   - Replace `your_groq_api_key_here` with your actual API key:
   ```env
   GROQ_API_KEY=gsk_your_actual_api_key_here
   ```

3. **Open Terminal/Command Prompt** in the project folder

4. **Run the application**:
   ```bash
   docker-compose up --build
   ```
   
   *This will download dependencies, build the app, and start it automatically*

5. **Access the app**: Open your browser and go to http://localhost:8501

6. **To stop the app**: Press `Ctrl+C` in the terminal

6. **To stop the app**: Press `Ctrl+C` in the terminal

### Alternative Docker Commands (Advanced Users):

**Build the image manually**:
```bash
docker build -t resume-critiquer .
```

**Run container directly**:
```bash
docker run -p 8501:8501 --env-file .env resume-critiquer
```

---

## 🐍 Method B: Local Python Setup

### What You Need:
- Python 3.8 or higher ([Download here](https://www.python.org/downloads/))
- Your Groq API key

### Step-by-Step Setup:

1. **Download/Clone this project** to your computer

2. **Open Terminal/Command Prompt** in the project folder

3. **Create a virtual environment** (Recommended):
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up your API key**:
   - Open the `.env` file
   - Replace `your_groq_api_key_here` with your actual API key:
   ```env
   GROQ_API_KEY=gsk_your_actual_api_key_here
   ```

6. **Run the application**:
   ```bash
   streamlit run app.py
   ```

7. **Access the app**: Open your browser and go to http://localhost:8501

---

## 🎯 How to Use the Application

1. **Upload Your Resume**:
   - Click "Browse files" button
   - Select your resume (PDF or TXT format)
   - Wait for upload to complete

2. **Specify Job Role** (Optional but Recommended):
   - Enter the job title you're targeting
   - Example: "Software Engineer", "Marketing Manager", "Data Analyst"
   - This provides more targeted feedback

3. **Analyze Your Resume**:
   - Click the "Analyze" button
   - Wait for AI analysis (usually 10-30 seconds)
   - Review the comprehensive feedback

4. **Review Results**:
   - **Overall Impression**: Quick summary of resume quality
   - **Strengths**: What's working well in your resume
   - **Areas for Improvement**: Specific issues to address
   - **Recommendations**: Concrete suggestions for enhancement
   - **Action Items**: Prioritized tasks (High/Medium/Low priority)
   - **Final Score**: Numerical rating with justification

---

## 🔧 Troubleshooting

### Common Issues:

**"API key not found" Error**:
- Ensure your `.env` file has the correct API key
- Check that there are no extra spaces or quotes around the key
- Restart the application after updating the API key

**"File has no content" Error**:
- Try a different PDF file
- Ensure your PDF contains selectable text (not just images)
- Try converting to TXT format if PDF doesn't work

**Docker Issues**:
- Ensure Docker Desktop is running
- Try `docker-compose down` then `docker-compose up --build`
- Check if port 8501 is already in use

**Slow Analysis**:
- This is normal for detailed analysis
- Wait up to 60 seconds for complex resumes
- Check your internet connection

---

## ⚙️ Technical Details

- **Framework**: Streamlit for web interface
- **AI Model**: Groq Llama-3.3-70b-versatile
- **File Processing**: PyPDF2 for PDF extraction
- **Environment**: Python 3.8+ with virtual environment support
- **Deployment**: Docker containerized for easy deployment

## 🤖 Supported AI Models

The application uses Groq's powerful language models:
- **Primary**: `llama-3.3-70b-versatile` (best quality)
- **Alternative**: `llama3-70b-8192`, `llama-3.1-8b-instant`

---

## � Support

If you encounter issues:
1. Check the troubleshooting section above
2. Ensure all prerequisites are met
3. Verify your API key is valid and active
4. Try restarting the application

---
