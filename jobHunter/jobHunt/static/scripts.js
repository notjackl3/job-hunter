function setJobDetail(button, title, description, company, date_posted, link) {
    document.getElementById('detail-title').innerText = title;
    document.getElementById('detail-company').innerText = company;
    document.getElementById('detail-description').innerText = description;
    document.getElementById('detail-date_posted').innerText = date_posted;
    document.getElementById('detail-link').innerText = 'Link to job';
    document.getElementById('detail-link').href = link;
}

document.getElementById("cover-letter-input").addEventListener("submit", function (event) {
    const resume = document.getElementById("resume-input").value;
    document.getElementById("resume-hidden").value = resume;
});

function showJobDetail(event) {
    const button = event.currentTarget;
    const title = button.dataset['title'];
    const description = button.dataset['description'];
    const company = button.dataset['company'];
    const date_posted = button.dataset['date_posted'];
    const link = button.dataset['link'];
    setJobDetail(button, title, description, company, date_posted, link);
    popUpJobDetail();
}

function initializeJobButtons() {
    const buttons = document.querySelectorAll('.job-button');
    buttons.forEach(function(button) {
        button.addEventListener('click', showJobDetail);
    });
}

function handleJobDescription(event) {
    const title = document.getElementById('detail-title').innerText;
    const company = document.getElementById('detail-company').innerText;
    const jobDescription = document.getElementById('detail-description').innerText;

    document.getElementById('title-hidden').value = title;
    document.getElementById('company-hidden').value = company;
    document.getElementById('job-description-hidden').value = jobDescription;
}

function dropdown() {
    document.getElementById("dropdown-content").classList.toggle("show");
}

function dropdown2() {
    document.getElementById("dropdown-content2").classList.toggle("show");
}

window.onclick = function(event) {
    if (!event.target.matches('.dropdown-button')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
        }
    }
    }
}

window.onclick = function(event) {
    if (!event.target.matches('.dropdown-button')) {
    var dropdowns = document.getElementsByClassName("dropdown-content2");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
        }
    }
    }
}

function updateQuery(key, value) {
    const url = new URL(window.location);
    url.searchParams.set(key, value); 
    window.location = url.href;      
}

function searchJob() {
    const job_query = document.getElementById("search").value;
    updateQuery('query', job_query);
}

function resetSearch() {
    updateQuery('query', "");
}

document.querySelectorAll(".delete-button").forEach(button => {
    button.addEventListener("click", async () => {
        const job_title = button.getAttribute("data-job-id");
        const confirmed = confirm("Are you sure you want to delete this job?");
        if (!confirmed) return;

        try {
            const response = await fetch(`delete/${job_title}/`, {
                method: "DELETE",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                }
            });

            if (response.status === 204) {
                button.closest(".job-post").remove();
            }
        } catch (error) {
            alert("Failed to delete job. Please try again.");
        }
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.getElementById('resume').style.display = "none";

document.getElementById('cover-letter-input').style.display = "none";
document.getElementById('cover-letter-input').addEventListener('submit', handleJobDescription);

window.addEventListener('DOMContentLoaded', initializeJobButtons);
