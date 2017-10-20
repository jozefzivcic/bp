google.charts.load('current', {packages: ['corechart', 'line']});
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
    var jsonUrl = getProtocolAndHost() + '/charts_data/base?test_id=' + String(testId);
    getJsonAndDrawChart(jsonUrl, drawLineChart);
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

function drawLineChart(jsonData) {
    const parsedPValues = jsonData['data'];
    const pValueString = document.getElementById('pvalue').getAttribute('value');
    const sequenceString = document.getElementById('seq').getAttribute('value');

    var data = new google.visualization.DataTable();
    data.addColumn('number', 'X');
    data.addColumn('number', pValueString);

    data.addRows(parsedPValues);

    var options = {
        hAxis: {
            title: sequenceString
        },

        vAxis: {
            title: pValueString,
            logScale: true,
            scaleType: "mirrorLog",
            minValue: 0.0,
            maxValue: 1.0,
            ticks: [{v: 0, f: '0'}, {v: 0.001, f: '0.001'}, {v: 0.01, f: '0.01'}, {v: 0.1, f: '0.1'}, {v: 1, f: '1'}]
        }
    };

    var formatter = new google.visualization.NumberFormat(
        {fractionDigits: 6});
    formatter.format(data, 1);

    var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
    chart.draw(data, options);
}
