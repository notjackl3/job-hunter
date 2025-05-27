ARG PYTHON_VERSION=3.11.9
FROM python:${PYTHON_VERSION}-slim AS base

WORKDIR /app

COPY ./jobHunter ./

EXPOSE 8000

RUN pip install --upgrade pip --no-cache-dir
RUN pip install -r /app/requirements.txt --no-cache-dir
RUN python3 manage.py collectstatic --noinput

# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "jobHunter.wsgi:application", "--bind", "0.0.0.0:8000"]

