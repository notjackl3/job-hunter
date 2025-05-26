function setJobDetail(button, title, description, company, date_posted, link) {
    document.getElementById('detail-title').innerText = title;
    document.getElementById('detail-company').innerText = company;
    document.getElementById('detail-description').innerText = description;
    document.getElementById('detail-date_posted').innerText = date_posted;
    document.getElementById('detail-link').innerText = 'Link to job';
    document.getElementById('detail-link').href = link;
}

function popUpJobDetail() {
    document.getElementById('job-detail-text').style.display = 'block';
    document.getElementById('resume-button').style.display = "block";
    document.getElementById('cover-letter-input').style.display = "none";
    document.getElementById('resume').style.display = "none";
}

function popUpResume() {
    document.getElementById('resume').style.display = "block";
    document.getElementById('cover-letter-input').style.display = "block";
    document.getElementById('job-detail-text').style.display = 'none';
    document.getElementById('resume-button').style.display = "none";
    console.log("popped up");
}

function enableElement(id) {
    if ( document.getElementById(id) ) {
        document.getElementById(id).removeAttribute("disabled");
        document.getElementById(id).className = "button bold";
    }
}