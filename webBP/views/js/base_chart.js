google.charts.load('current', {packages: ['corechart', 'line']});
google.charts.setOnLoadCallback(drawBasic);

function drawBasic() {

    var data = new google.visualization.DataTable();
    data.addColumn('number', 'X');
    data.addColumn('number', 'p-value');

    data.addRows([
        [1, 0.173564], [2, 0.0021], [3, 0.181066], [4, 0.469225], [5, 0.363090], [6, 0.075491], [7, 0.024652], [8, 0.078436], [9, 0.117400], [10, 0.634010], [11, 0.01], [12, 0.173564], [13, 0.074901], [14, 0.181066], [15, 0.469225], [16, 0.363090], [17, 0.075491], [18, 0.024652], [19, 0.078436], [20, 0.117400], [21, 0.634010], [22, 0.01], [23, 0.173564], [24, 0.074901], [25, 0.181066], [26, 0.469225], [27, 0.363090], [28, 0.075491], [29, 0.024652], [30, 0.078436], [31, 0.117400], [32, 0.634010], [33, 0.01]
    ]);

    var options = {
        hAxis: {
            title: 'num'
        },

        vAxis: {
            title: 'p-value',
            logScale: true,
            scaleType: "mirrorLog",
            minValue: 0.0,
            maxValue: 1.0,
            ticks: [{v: 0, f: '0'}, {v: 0.001, f: '0.001'}, {v: 0.01, f: '0.01'}, {v: 0.1, f: '0.1'}, {v: 1, f: '1'}],
            gridlines: {}
        }
    };
    var formatter = new google.visualization.NumberFormat(
        {fractionDigits: 6});
    formatter.format(data, 1);
    var chart = new google.visualization.LineChart(document.getElementById('chart_div'));

    chart.draw(data, options);
}