# Base Python image
FROM python:3.11

# Set env flags for clean output and no .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /code

# Copy everything from the host into the container
COPY . /code/

# Install dependencies from requirements.txt inside jobHunter/
RUN pip install --upgrade pip
RUN pip install -r jobHunter/requirements.txt
RUN python3 -m nltk.downloader punkt_tab averaged_perceptron_tagger_eng stopwords wordnet

# Set working directory to where manage.py is
WORKDIR /code/jobHunter
