from django.shortcuts import render, redirect
from django.http import FileResponse, HttpResponse
from django.db import connection
from .jobscrape import scrape
from .coverletter import write
from .models import JobPost
from collections import Counter
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
import re
from rest_framework.decorators import api_view


# import nltk
# import ssl
# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context
#     nltk.download('wordnet')
#     nltk.download('omw-1.4')


popular_languages = [
    "python",
    "javascript",
    "typescript",
    "java",
    "c",
    "c#",
    "c++",
    "go",
    "typescript",
    "ruby",
    "swift",
    "php",
    "rust",
    "sql",
    "perl",
    "html",
    "css",
    "assembly",
    "matlab",
    "kotlin",
    "r"
]

popular_technologies = [
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "git",
    "github",
    "gitlab",
    "bitbucket",
    "jira",
    "jenkins",
    "circleci",
    "travisci",
    "linux",
    "bash",
    "mysql",
    "postgresql",
    "mongodb",
    "sqlite",
    "redis",
    "elasticsearch",
    "firebase",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "pandas",
    "numpy",
    "react",
    "angular",
    "vue",
    "django",
    "flask",
    "spring",
    "node",
    "express",
    "fastapi",
    "graphql",
    "rest",
    "webpack",
    "npm",
    "yarn",
    "tailwind",
    "bootstrap"
]

lemmatizer = WordNetLemmatizer()


def get_wordnet_pos(tag):
    if tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN


def detect_action_words(text):
    tokens = word_tokenize(text.lower())
    words = [word for word in tokens if word.isalpha()]
    tagged = nltk.pos_tag(words)
    stop_words = set(stopwords.words('english'))

    action_words = [
        lemmatizer.lemmatize(word, get_wordnet_pos(tag))
        for word, tag in tagged
        if tag.startswith('VB') and word not in stop_words
    ]
    return action_words


def home(request):
    existing_job_posts = []
    sort_by = request.GET.get("sort", "date_posted")
    direction = request.GET.get("direction", "ASC")
    ordering = f"{'' if direction == 'ASC' else '-'}{sort_by}"
    # with connection.cursor() as cursor:
    #     cursor.execute(f"""
    #         SELECT title, company, date_posted, description, keywords, link
    #         FROM "jobHunt_jobpost"
    #         ORDER BY {sort_by} {direction};
    #         """)
    #     results = cursor.fetchall()
    #     for result in results:
    #         existing_job_posts.append({"title": result[0],
    #                                    "company": result[1],
    #                                    "date_posted": result[2],
    #                                    "description": result[3],
    #                                    "keywords": result[4],
    #                                    "link": result[5]})
    existing_job_posts = JobPost.objects.all().order_by(ordering)
    if existing_job_posts:
        context = {"job_posts": existing_job_posts}
        return render(request, "index.html", context)
    else:
        return render(request, "index.html")


def add_job(request):
    query = request.POST.get("query")
    city = request.POST.get("city")
    country = request.POST.get("country")
    result_num = 100
    hours_old = request.POST.get("hours_old")
    scrape(query, city, country, result_num, hours_old)
    # job_posts = scrape(query, city, country, result_num, hours_old)
    # context = {"job_posts": job_posts}
    # return render(request, 'index.html', context)
    # job_posts = []
    # with connection.cursor() as cursor:
    #     cursor.execute("""
    #         SELECT title, company, date_posted, description, keywords, link
    #         FROM "jobHunt_jobpost";
    #         """)
    #     results = cursor.fetchall()
    #     for result in results:
    #         job_posts.append({"title": result[0],
    #                           "company": result[1],
    #                           "date_posted": result[2],
    #                           "description": result[3],
    #                           "keywords": result[4],
    #                           "link": result[5]})
    # request.session['job_posts'] = job_posts
    return redirect("/home")


def write_cover_letter(request):
    job_description = request.POST.get("job-description-hidden")
    resume = request.POST.get("resume-hidden")
    file_data = write(job_description, resume)
    response = HttpResponse(file_data, content_type='application/text charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="cover-letter.txt"'
    return response


def show_statistics(request):
    descriptions = JobPost.objects.values_list('description', flat=True)
    languages = []
    technologies = []
    words = []
    for row in descriptions:
        action_words = detect_action_words(row)
        action_words = [x for x in action_words if x.lower() != "work"]  # this word is too common
        temp = re.split(r'[ ,.;\'\"!/()]', row)

        words.extend(action_words)
        languages.extend([x.lower() for x in temp if x.lower() in popular_languages])
        technologies.extend([x.lower() for x in temp if x.lower() in popular_technologies])

    Counters_found = Counter(languages)
    most_occur_languages = Counters_found.most_common()
    Counters_found = Counter(technologies)
    most_occur_technologies = Counters_found.most_common(20)
    Counters_found = Counter(words)
    most_occur_words = Counters_found.most_common(20)

    languages_list = [x[0] for x in most_occur_languages]
    languages_freq = [x[1] for x in most_occur_languages]
    technologies_list = [x[0] for x in most_occur_technologies]
    technologies_freq = [x[1] for x in most_occur_technologies]
    words_list = [x[0] for x in most_occur_words]
    words_freq = [x[1] for x in most_occur_words]

    dates_posted = JobPost.objects.values_list('date_posted', flat=True)
    dates = [date.strftime('%Y-%m-%d') for date in dates_posted if date is not None]

    Counters_found = Counter(dates)
    most_occur_dates = Counters_found.most_common()
    most_occur_dates.sort(key=lambda x: x[0])

    dates_list = [x[0] for x in most_occur_dates]
    dates_freq = [x[1] for x in most_occur_dates]

    context = {"languages_list": json.dumps(languages_list), "languages_freq": json.dumps(languages_freq),
               "technologies_list": json.dumps(technologies_list), "technologies_freq": json.dumps(technologies_freq),
               "words_list": json.dumps(words_list), "words_freq": json.dumps(words_freq),
               "dates_list": dates_list, "dates_freq": dates_freq}

    return render(request, "statistics.html", context)


from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes

@api_view(["DELETE"])
@permission_classes([AllowAny])
def delete_job(request, id):
    try:
        job = JobPost.objects.get(id=id)
        job.delete()
        return Response({"message": "Job deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except JobPost.DoesNotExist:
        return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

