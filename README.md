# job-hunter 🔎
This Django web app helps you search for jobs within the tech industry. It will help you find, manage and filter out the most updated jobs on platforms including `LinkedIn`, `Indeed`, and `Google`. Additionally, it writes cover letter in a blink of an eye. Lastly, statistics about job demands will be shown.

*(I spent a lot of time scrolling through countless platforms to search for jobs. Thus, I wanted to create an app which scrapes the internet and returns the latest job posts. Along the way, I figured that having information about the most popular techlogies will be useful, and also the ability to write cover letter).*

## Features

- User authentication and password reset via email.
- Scrape job opportunities based on keywords, location, and upload dates.
- Allow job posts management and filtering.
- Write tailored cover letters.
- Display job market information (posting dates, most common languages, technologies, keywords).

## How It's Made:

**Tech used:** Python, Django, HTML, CSS, JavaScript, PostgreSQL, AWS EC2.

This app is built using Django for the backend, with `supabase` as the primary database. On the other hand, the frontend is made with HTML, CSS, JavaScript and hosted on AWS EC2.

The user authentication system is managed using Django’s built-in `authentication system` and `regex`. Additional tools like `jobspy2` handle web scraping tasks across platforms. Moreover, it integrates the `openai` api to generate personalized cover letters based on job descriptions and resume. Besides, the `nltk` module is used for keyword extractions and analysis, while `matplotlib` and `chart.js` allow graphical visualisations.

## What I Learned Through This Project:

- Django authentication system.
- Web scraping techniques.
- Collect data and build up real-time charts.
- Deploy app using AWS EC2.
- REST api structure, communications between front-end and back-end.

