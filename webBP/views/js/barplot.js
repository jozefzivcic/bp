google.charts.load("current", {packages: ['corechart']});
google.charts.setOnLoadCallback(createChart);

function getTestId() {
    var url = window.location.href;
    var testIdString = /test_id=([^&]+)/.exec(url)[1];
    if (testIdString === undefined)
        return undefined;
    try {
        var testId = parseInt(testIdString);
    } catch (err) {
        return undefined;
    }
    return testId;
}

function getProtocolAndHost() {
    return window.location.protocol + '//' + window.location.host;
}

function errFunction(err) {
    if (err !== null) {
        alert('An error occurred while downloading data for chart (' + err + ')');
    } else {
        alert('An error occurred while downloading data for chart');
    }
}

function createChart() {
    var testId = getTestId();
    var jsonUrl = getProtocolAndHost() + '/charts_data/barplot?test_id=' + String(testId);
    getJsonAndDrawChart(jsonUrl, drawBarplot);
}

function getJsonAndDrawChart(url, callback) {
    var request = new XMLHttpRequest();
    request.open('GET', url, true);
    request.send(null);

    var handler = function () {
        if (request.readyState === 4) {
            if (request.status === 200) {
                const obj = JSON.parse(request.responseText);
                callback(obj);
            } else
                errFunction(request.status);
        }
    };

    request.onreadystatechange = handler;
    request.send(null);
}

function drawBarplot(jsonData) {
    const titleString = document.getElementById("title").getAttribute("value");
    arr = [["group", "num"]].concat(jsonData["data"]);

    var data = google.visualization.arrayToDataTable(arr);

    var view = new google.visualization.DataView(data);
    view.setColumns([0, 1,
        {
            calc: "stringify",
            sourceColumn: 1,
            type: "string",
            role: "annotation"
        }]);

    var options = {
        title: titleString,
        bar: {groupWidth: "75%"},
        legend: {position: "none"},
        hAxis: {
            minValue: 0,
            maxValue: 10
        },
        vAxis: {
            minValue: 0
        }
    };
    var chart = new google.visualization.ColumnChart(document.getElementById("chart_div"));
    chart.draw(view, options);
}