const ctx = document.getElementById('chart').getContext('2d');
var ticker_symbol = document.getElementById("ticker_symbol");
var ticker_name = document.getElementById("ticker_name");
var ticker_value = document.getElementById("ticker_value");
var sell_button =  document.getElementById("sell_button");
var buy_button = document.getElementById("buy_button");
var form = document.getElementById("buy_form");
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

Array.prototype.contains = function ( str ) {
    return this.indexOf(str) > -1;
}

Object.prototype.keys = function () {
    return Object.keys(this);
}

add_watchlist.addEventListener("click", function(e) {
    e.preventDefault();
    console.log("add to watchlist");
})

document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.modal');
    var instances = M.Modal.init(elems);
});

function buy_market() {
    shares = document.getElementsByName("number_shares")[0].value;
    console.log(`shares ${shares}`);
    return false;
}

socket.on('connect', function () {
    console.log("connected");
    var sec_id = window.location.pathname;
    socket.emit("get_security_info", [sec_id.split("/")[2]]);
});

socket.on('return_stock_info', function (data) {
    console.log("return stock search");
    console.dir(data);    
    var graph = data[0];
    var info = data[1];
    var position = data[2];
    ticker_symbol.innerHTML = '';
    ticker_name.innerHTML = '';
    ticker_value.innerHTML = '';
    activities.innerHTML = '';
    about.innerHTML = '';

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

    if ( position.keys().contains(info.id) ) {
        // this security is owned by you
        console.log("you dont own this security")
        sell_button.style.display = 'inline-block';
    } else {
        console.log("you dont own this security")
    }

    var ticker_symbol_text = document.createTextNode(info.stock.symbol);
    ticker_symbol.appendChild(ticker_symbol_text);
    var ticker_name_text = document.createTextNode(info.stock.name);
    ticker_name.appendChild(ticker_name_text);
    var ticker_value_text = document.createTextNode(`${parseFloat(info.quote.amount).toFixed(2)} ${info.quote.currency}`);
    ticker_value.appendChild(ticker_value_text);
    var about_text = document.createTextNode(info.fundamentals.description);
    about.appendChild(about_text);
    
    for (const stock_chart of graph.results.slice(1)) {
        var date = new Date('1970-01-01T' +stock_chart.time  + 'Z');
        chart.data.labels.push(date.toLocaleTimeString({},
            { timeZone:'UTC',hour12:true,hour:'numeric',minute:'numeric'}
        ));
        chart.data.datasets.forEach((dataset) => {
            dataset.data.push(stock_chart.adj_close);
        });
        chart.update();
    }

    socket.emit("get_security_info", [info.id]);
});