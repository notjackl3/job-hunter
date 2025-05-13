from django.shortcuts import render, redirect
from django.http import FileResponse, HttpResponse
from django.urls import reverse
from .jobscrape import scrape
from .coverletter import write
from .models import JobPost
from collections import Counter
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer

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
    "node.js",
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
        return wordnet.NOUN  # default


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
    existing_job_posts = request.session.get('job_posts')
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
    job_posts = scrape(query, city, country, result_num, hours_old)
    # context = {"job_posts": job_posts}
    # return render(request, 'index.html', context)
    request.session['job_posts'] = job_posts
    return redirect("/home")


def write_cover_letter(request):
    job_description = request.POST.get("job-description")
    file_data = write(job_description,
                      "/Users/notjackl3/Documents/job-hunter/jobHunter/jobHunt/static/Huu An Duc (Jack) Le Resume.pdf")
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
        action_words = [x for x in action_words if x != "work"]  # this word is too common
        temp = row.split()

        words.extend(action_words)
        languages.extend([x.lower() for x in temp if x.lower() in popular_languages])
        technologies.extend([x.lower() for x in temp if x.lower() in popular_technologies])

    Counters_found = Counter(languages)
    most_occur_languages = Counters_found.most_common()
    Counters_found = Counter(technologies)
    most_occur_technologies = Counters_found.most_common()
    Counters_found = Counter(words)
    most_occur_words = Counters_found.most_common(20)

    languages_list = [x[0] for x in most_occur_languages]
    languages_freq = [x[1] for x in most_occur_languages]
    technologies_list = [x[0] for x in most_occur_technologies]
    technologies_freq = [x[1] for x in most_occur_technologies]
    words_list = [x[0] for x in most_occur_words]
    words_freq = [x[1] for x in most_occur_words]

    context = {"languages_list": json.dumps(languages_list), "languages_freq": json.dumps(languages_freq),
               "technologies_list": json.dumps(technologies_list), "technologies_freq": json.dumps(technologies_freq),
               "words_list": json.dumps(words_list), "words_freq": json.dumps(words_freq)}

    return render(request, "statistics.html", context)
