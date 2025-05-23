from openai import OpenAI
from dotenv import load_dotenv
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


def write(title, company, job_description, resume):
    resume_extractor = client.chat.completions.create(
        model=GPT_MODEL,
        messages=[
            {
                "role": "system",
                "content": WRITING_PROMPT
            },
            {
                "role": "user",
                "content": f"Position: {title}, Company: {company}, Job description: {job_description}. Resume: {resume}"
            }
        ],
        temperature=WRITING_CREATIVITY,
        top_p=WRITING_ACCURACY
    )
    return resume_extractor.choices[0].message.content
