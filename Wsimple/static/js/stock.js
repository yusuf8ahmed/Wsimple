const ctx = document.getElementById('chart').getContext('2d');
var ticker_symbol = document.getElementById("ticker_symbol");
var ticker_name = document.getElementById("ticker_name");
var ticker_value = document.getElementById("ticker_value");
var buy = document.getElementById("buy");
var sell = document.getElementById("sell");
var add_watchlist = document.getElementById("add_watchlist");
var stats = document.getElementById("stats");
var activities = document.getElementById("activities");
var about = document.getElementById("about");
var gradient = ctx.createLinearGradient(0, 0, 0, 350);
gradient.addColorStop(0, 'rgba(138, 192, 189, 1)');
gradient.addColorStop(1, 'rgba(138, 192, 189, 0)');
var socket = io();

document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.modal');
    var instances = M.Modal.init(elems);
});

socket.on('connect', function () {
    console.log("connected");
    var sec_id = window.location.pathname;
    socket.emit("get_security_info", [sec_id.split("/")[2]]);
});

socket.on('return_stock_info', function (data) {
    ticker_symbol.innerHTML = '';
    ticker_name.innerHTML = '';
    ticker_value.innerHTML = '';
    activities.innerHTML = '';
    about.innerHTML = '';
    console.log("return stock search");
    console.dir(data);

    var chart = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [{
                label: "stock value",
                backgroundColor: gradient,
                borderColor: "#8AC0BD",
                strokeColor: "#8AC0BD",
                pointColor: "#8AC0BD",
                pointStrokeColor: "#8AC0BD",
                pointHighlightFill: "#8AC0BD",
                data: []
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            legend: {
                display: false
            },
            animation: {
                duration: 0 // general animation time
            },
            hover: {
                animationDuration: 0 // duration of animations when hovering an item
            },
            responsiveAnimationDuration: 0, // animation duration after a resize
            scales: {
                xAxes: [{
                    gridLines: {
                        display: false
                    }
                }],
                yAxes: [{
                    gridLines: {
                        display: false
                    },
                    ticks: {
                        callback: function(value) {if (value % 1 === 0) {return value;}}
                    }
                }]
            }
        }
    });

    var ticker_symbol_text = document.createTextNode(data[1].stock.symbol);
    ticker_symbol.appendChild(ticker_symbol_text);
    var ticker_name_text = document.createTextNode(data[1].stock.name);
    ticker_name.appendChild(ticker_name_text);
    var ticker_value_text = document.createTextNode(`${parseFloat(data[1].quote.amount).toFixed(2)} ${data[1].quote.currency}`);
    ticker_value.appendChild(ticker_value_text);
    var about_text = document.createTextNode(data[1].fundamentals.description);
    about.appendChild(about_text);
    
    for (const stock_chart of data[0].results.slice(1)) {
        var date = new Date('1970-01-01T' +stock_chart.time  + 'Z');
        chart.data.labels.push(date.toLocaleTimeString({},
            { timeZone:'UTC',hour12:true,hour:'numeric',minute:'numeric'}
        ));
        chart.data.datasets.forEach((dataset) => {
            dataset.data.push(stock_chart.adj_close);
        });
        chart.update();
    }

    socket.emit("get_security_info", [data[1].id]);
});