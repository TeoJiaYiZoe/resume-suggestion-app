from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import requests
import PyPDF2
import json

app = FastAPI()

# CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:5173"],  # Adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Replace this with your actual DeepSeek API key
API_KEY = 'API_KEY'  
api_url = 'https://api.deepseek.com/chat/completions'

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {API_KEY}'
}

async def get_deepseek_response(prompt: str):
    data = {
        'model': 'deepseek-chat',
        'messages': [
            {'role': 'system', 'content': 'You are a helpful resume editor who specializes in editing resumes to fit job descriptions.'},
            {'role': 'user', 'content': prompt}
        ],
        'stream': False
    }

    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"DeepSeek API error: {str(e)}")


def extract_pdf_text(pdf_file: UploadFile):
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file.file)
        pdf_text = ""
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                pdf_text += text
        return pdf_text.strip()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading PDF: {str(e)}")


@app.post("/process_resume/")
async def process_resume(
    description: str = Form(...), 
    resume_file: Optional[UploadFile] = None
):
    resume_text = ""

    if resume_file:
        resume_file.file.seek(0)
        resume_text = extract_pdf_text(resume_file)

    prompt = f"""
    Job Description:
    {description}

    Resume:
    {resume_text}

    Task: You are an AI specialized in analyzing resumes and tailoring them to specific job descriptions.
    """

    response = await get_deepseek_response(prompt)
    
    return {"response": response}
