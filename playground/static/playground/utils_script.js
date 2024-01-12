
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
async function postData(data, url = "") {
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
        body: JSON.stringify({
            userId: data,
        }
        ), // body data type must match "Content-Type" header
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


/*
{
    var outletCount = 0; //global variable to get the no of outlets
    var data = [{
        "outlet": "JAYANAGAR",
        "cancelled": 126544,
        "duplicate": 1
    },
    {
        "outlet": "MALLESHWARAM",
        "cancelled": 31826,
        "duplicate": 31
    },
    {
        "outlet": "KOLAR",
        "cancelled": 10374,
        "duplicate": 10
    },
    {
        "outlet": "New Test",
        "cancelled": 154,
        "duplicate": 20
    }
    ];

    let formatData = function (data) { //outlets is unique thats why formating it to loop forward in my code
        let outlets = [];
        data.forEach(element => {
            if (outlets.indexOf(element.outlet) == -1) {
                outlets.push(element.outlet);
            }
        });
        outletCount = outlets.length //calculating outlet count

        return {
            data: data,
            outlets: outlets,

        };
    };

    let renderTable = function (data) {
        outlets = data.outlets;
        data = data.data;
        let tbl = document.getElementById("tblOlSalesSummary");
        let table = document.createElement("table");
        let thead = document.createElement("thead");
        let headerRow = document.createElement("tr");
        let th = document.createElement("th");
        th.innerHTML = "Bill Type"; //header
        th.classList.add("text-center");
        headerRow.appendChild(th);
        th = document.createElement("th");
        th.innerHTML = "Average"; //header
        th.classList.add("text-center");
        headerRow.appendChild(th);
        outlets.forEach(element => {
            th = document.createElement("th");
            th.innerHTML = element; //this one is populating outlet as header
            th.classList.add("text-center");

            headerRow.appendChild(th);

        });

        thead.appendChild(headerRow);
        table.appendChild(thead);

        let tbody = document.createElement("tbody"); // from here onwards i don't know what to do

        let row = document.createElement("tr");

        let total = 0;

        // static field insertion for Cancelled bill
        let el = 'Cancelled bill';
        td = document.createElement("td");
        td.innerHTML = el.toLocaleString('en-in');
        td.classList.add("text-right");
        row.appendChild(td);
        // Logic start to find the average cancelled amount 
        var total_cancel = 0;
        total_can_count = 0;
        outlets.forEach(outlet => {
            data.forEach(d => {
                if (d.outlet == outlet) {
                    total_cancel += parseInt(d.cancelled);
                    total_can_count++;

                }
            });
        });

        let el_avg = (total_cancel / (total_can_count));
        td = document.createElement("td");
        td.innerHTML = el_avg.toLocaleString('en-in');
        td.classList.add("text-right");
        row.appendChild(td);
        // Logic End to find the average cancelled amount 

        outlets.forEach(outlet => {
            let el = 0;
            data.forEach(d => {
                if (d.outlet == outlet) {
                    total += parseInt(d.cancelled);
                    el = d.cancelled;
                }
            });
            td = document.createElement("td");
            td.innerHTML = el.toLocaleString('en-in');
            td.classList.add("text-right");
            row.appendChild(td);
        });

        tbody.appendChild(row);

        let row_duplicate = document.createElement("tr");

        let total_dup = 0;
        // static field insertion for duplicate bill
        let el_2 = 'Duplicate bill';
        td = document.createElement("td");
        td.innerHTML = el_2.toLocaleString('en-in');
        td.classList.add("text-right");
        row_duplicate.appendChild(td);

        // Logic start to find the Duplicate average  
        total_dup_count = 0;
        outlets.forEach(outlet => {
            data.forEach(d => {
                if (d.outlet == outlet) {
                    total_dup += parseInt(d.duplicate);
                    total_dup_count++;
                }
            });
        });

        let el_avg_2 = (total_dup / (total_dup_count));
        td = document.createElement("td");
        td.innerHTML = el_avg_2.toLocaleString('en-in');
        td.classList.add("text-right");
        row_duplicate.appendChild(td);

        // Logic End to find the Duplicate average  

        outlets.forEach(outlet => { //i am trying to loop through outlets but getting somthing else
            let el = 0;
            data.forEach(d => {
                if (d.outlet == outlet) {
                    total += parseInt(d.duplicate);
                    el = d.duplicate;
                }
            });
            td = document.createElement("td");
            td.innerHTML = el.toLocaleString('en-in');
            td.classList.add("text-right");
            row_duplicate.appendChild(td);
        });


        tbody.appendChild(row);
        tbody.appendChild(row_duplicate);

        table.appendChild(tbody);
        tbl.innerHTML = "";
        tbl.appendChild(table);
        table.classList.add("table");
        table.classList.add("table-striped");
        table.classList.add("table-bordered");
        table.classList.add("table-hover");
    }
    let formatedData = formatData(data);
    renderTable(formatedData);

}
*/