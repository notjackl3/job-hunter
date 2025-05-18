import csv
import tempfile
import pandas as pd
from jobspy2 import scrape_jobs
from .models import JobPost
from django.db import connection
from datetime import datetime
import pycountry


def delete_duplicate_jobs():
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM "jobHunt_jobpost"
            WHERE id NOT IN (
              SELECT MIN(id)
              FROM "jobHunt_jobpost"
              GROUP BY title
            );
        """)


def scrape(query: str, city: str, country: str, results_num: int, hours_old: int = 366):
    jobs = scrape_jobs(
        site_name=["indeed", "linkedin", "glassdoor", "google"],
        search_term=query,
        location=f"{city}, {country}",
        country_indeed=country,
        results_wanted=results_num,
        hours_old=hours_old,

        linkedin_fetch_description=True
        # proxies=["208.195.175.46:65095", "208.195.175.45:65095", "localhost"],
    )
    print(f"Found {len(jobs)} jobs")
    with tempfile.TemporaryDirectory() as temp_dir:
        output_file = f"{temp_dir}/jobs.csv"
        jobs.to_csv(output_file, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)
        # write_doc(output_file)

        df = pd.read_csv(output_file)

        # job_posts = []
        for index, row in df.iterrows():
            title = row["title"]
            company = row["company"]
            date_posted = row["date_posted"]
            try:
                date = datetime.strptime(date_posted, "%Y-%m-%d").date()
            except ValueError:
                date = None
            except TypeError:
                date = None
            description = row["description"]
            keywords = ""
            link = row["job_url"]
            location = row["location"]
            country = pycountry.countries.search_fuzzy(location.split(",")[-1])[0].name

            if not JobPost.objects.filter(title=title).exists():
                new_post = JobPost(site=row["site"],
                                title=title,
                                company=company,
                                date_posted=date,
                                description=description,
                                location=country,
                                keywords=keywords,
                                link=link)
                new_post.save()

        delete_duplicate_jobs()
