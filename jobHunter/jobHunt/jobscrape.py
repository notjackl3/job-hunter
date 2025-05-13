import csv
import tempfile
import pandas as pd
from jobspy import scrape_jobs
from .models import JobPost
from django.db import connection


# def job_exists(title, company, date_posted):
#     with connection.cursor() as cursor:
#         cursor.execute("""
#             SELECT * FROM "jobHunt_jobpost"
#             WHERE title = %s AND company = %s
#             LIMIT 1
#         """, [title, company, date_posted])
#         result = cursor.fetchone()


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

        job_posts = []
        for index, row in df.iterrows():
            title = row["title"]
            company = row["company"]
            date_posted = row["date_posted"]
            description = row["description"]
            keywords = ""
            link = row["job_url"]

            new_post = JobPost(site=row["site"],
                               title=title,
                               company=company,
                               date_posted=date_posted,
                               description=description,
                               location=row["location"])
            new_post.save()

            job_posts.append({"title": title,
                              "company": company,
                              "date_posted": date_posted,
                              "description": description,
                              "keywords": keywords,
                              "link": link})

        delete_duplicate_jobs()

        return job_posts
