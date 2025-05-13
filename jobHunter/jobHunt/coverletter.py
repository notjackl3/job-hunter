from openai import OpenAI
from dotenv import load_dotenv
import textract
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
GPT_MODEL = "gpt-3.5-turbo"
WRITING_PROMPT = ("You will act as a helpful, smart hiring manager. You will be given a job description and a resume."
                  "Your job is to write a cover for that job, based on the experiences in the resume. Make sure to be"
                  "inspiring and semi-formal, do not flex grades or projects that much, truly show your passionate "
                  "towards the job. Also, don't just list out the requirements, ensure the language is natural.")
WRITING_CREATIVITY = 0.7
WRITING_ACCURACY = 0.8


def extract_text_from_pdf(file):
    extracted_resume_text = textract.process(file, method='pdfminer').decode('utf-8')
    return extracted_resume_text


def write(job_description, resume):
    resume_extractor = client.chat.completions.create(
        model=GPT_MODEL,
        messages=[
            {
                "role": "system",
                "content": WRITING_PROMPT
            },
            {
                "role": "user",
                "content": f"Job description: {job_description}. Resume: {extract_text_from_pdf(resume)}"
            }
        ],
        temperature=WRITING_CREATIVITY,
        top_p=WRITING_ACCURACY
    )
    return resume_extractor.choices[0].message.content
