
function is_audio_file_type(type) {
    let result = false;
    switch (type) {
        case 'audio/aac':
        case 'audio/mpeg':
        case 'audio/wav':
        case 'audio/webm':
        case 'audio/x-flac':
        case 'audio/flac':
            result = true;
    }
    return result;
}


// Example POST method implementation:
async function postData(form,data, url="") {
    let csrftoken = getCookie('csrftoken');
    // Default options are marked with *
    const response = await fetch(url, {
        method: "POST", // *GET, POST, PUT, DELETE, etc.
        mode: "cors", // no-cors, *cors, same-origin
        cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        credentials: "same-origin", // include, *same-origin, omit
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        redirect: "follow", // manual, *follow, error
        referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        body: JSON.stringify(data), // body data type must match "Content-Type" header
    });
    return response.json(); // parses JSON response into native JavaScript objects
}

// Example POST method implementation:
async function postFile(file, url = "") {
    let csrftoken = getCookie('csrftoken');
    const response = await fetch(url, {
        method: "POST", // *GET, POST, PUT, DELETE, etc.
        mode: "cors", // no-cors, *cors, same-origin
        cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        credentials: "include", // include, *same-origin, omit
        headers: {
            "X-CSRFToken": csrftoken
        },
        files: file,
        data: file
    });
    return response.json(); // parses JSON response into native JavaScript objects
}

// Example POST method implementation:
async function postForm(form, url = "") {
    let csrftoken = getCookie('csrftoken');
    const response = await fetch(url, {
        method: "POST", // *GET, POST, PUT, DELETE, etc.
        mode: "cors", // no-cors, *cors, same-origin
        cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        credentials: "include", // include, *same-origin, omit
        headers: {
            "X-CSRFToken": csrftoken
        },
        body: form
    });
    return response.json(); // parses JSON response into native JavaScript objects
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
