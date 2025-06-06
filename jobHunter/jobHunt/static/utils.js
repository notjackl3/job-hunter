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