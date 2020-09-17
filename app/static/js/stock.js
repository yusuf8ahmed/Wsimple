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
// stats line 1
var high = document.getElementById("high");
var whigh = document.getElementById("whigh");
var low = document.getElementById("low");
var wlow = document.getElementById("wlow");
// line 2
var open = document.getElementById("open");
var mktcap = document.getElementById("mktcap");
var vol = document.getElementById("vol");
var avgvol = document.getElementById("avgvol");
// line 3
var pe = document.getElementById("pe");
var yield_ = document.getElementById("yield");
var exg = document.getElementById("exg");
var beta = document.getElementById("beta");
// line 4
var debt = document.getElementById("debt");
var revenue = document.getElementById("revenue");
var tassets = document.getElementById("tassets");
var gpm = document.getElementById("gpm");
// line 5
var cash_ = document.getElementById("cash");
var growth = document.getElementById("growth");
var ceo = document.getElementById("ceo");
var website = document.getElementById("website");
gradient.addColorStop(0, 'rgba(138, 192, 189, 1)');
gradient.addColorStop(1, 'rgba(138, 192, 189, 0)');
var socket = io("/stock");

Array.prototype.contains = function (str) {
    return this.indexOf(str) > -1;
};

Object.prototype.keys = function () {
    return Object.keys(this);
};

add_watchlist.addEventListener("click", function(e) {
    e.preventDefault();
    console.log("add to watchlist");
});

function buy_market() {
    shares = document.getElementsByName("number_shares")[0].value;
    console.log(`shares ${shares}`);
    return false;
}

function display_stock() {
    high.innerHTML = ''; whigh.innerHTML = ''; low.innerHTML = ''; wlow.innerHTML = '';
    open.innerHTML = ''; mktcap.innerHTML = ''; vol.innerHTML = ''; avgvol.innerHTML = '';
    pe.innerHTML = ''; yield_.innerHTML = ''; exg.innerHTML = ''; beta.innerHTML = '';
    debt.innerHTML = ''; revenue.innerHTML = ''; tassets.innerHTML = ''; gpm.innerHTML = '';
    cash.innerHTML = ''; growth.innerHTML = ''; ceo.innerHTML = ''; website.innerHTML = '';

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
        console.log("you own this security");
        sell_button.style.display = 'inline-block';
    } else {
        console.log("you dont own this security");
    }

    high.innerHTML = parseFloat(info.quote.high).toFixed(2);    
    whigh.innerHTML = info.fundamentals.high_52_week.toFixed(2);
    low.innerHTML = parseFloat(info.quote.low).toFixed(2);      
    wlow.innerHTML = info.fundamentals.low_52_week.toFixed(2);
    open.innerHTML = parseFloat(info.quote.open).toFixed(2);    
    mktcap.innerHTML = info.fundamentals.market_cap.toFixed(2);
    vol.innerHTML = info.quote.volume;   
    avgvol.innerHTML = parseFloat(info.stock.avg_daily_volume_last_month).toFixed(2);
    pe.innerHTML = info.fundamentals.pe_ratio;   
    yield_.innerHTML = `${info.fundamentals.yield * 100}%`;
    exg.innerHTML = info.stock.primary_exchange; 
    beta.innerHTML = info.fundamentals.beta;
    debt.innerHTML = info.fundamentals.company_debt;    
    revenue.innerHTML = info.fundamentals.company_revenue;
    tassets.innerHTML = info.fundamentals.total_assets; 
    gpm.innerHTML = info.fundamentals.company_gross_profit_margin;
    cash_.innerHTML = info.fundamentals.company_cash;    
    growth.innerHTML = info.fundamentals.company_earnings_growth;
    ceo.innerHTML = info.fundamentals.company_ceo;  
    
    var stats_website_link = document.createElement("a");
    stats_website_link.setAttribute("target", "_blank");
    stats_website_link.setAttribute("href", `${info.fundamentals.website}`);
    var stats_website_text = document.createTextNode("Website");
    stats_website_link.appendChild(stats_website_text);
    website.appendChild(stats_website_link);

    var ticker_symbol_text = document.createTextNode(info.stock.symbol);
    var ticker_name_text = document.createTextNode(info.stock.name);
    var ticker_value_text = document.createTextNode(`${parseFloat(info.quote.amount).toFixed(2)} ${info.quote.currency}`);
    var about_text = document.createTextNode(info.fundamentals.description);
    ticker_symbol.appendChild(ticker_symbol_text);
    ticker_name.appendChild(ticker_name_text);
    ticker_value.appendChild(ticker_value_text);
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

}

function display_etf() {

}

socket.on('invalid_token', function (data) {
    alert("Access Token is Invalid or Broken must return to login page");
    window.location.href = "/";
});

socket.on('connect', function () {
    console.log("connected");
    var sec_id = window.location.pathname;
    socket.emit("get_security_info", sec_id.split("/")[2]);
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

    if (info.security_type == "us_stocks" || "canadian_stocks") {
        display_stock();
        console.log("stock");
    } else if (info.security_type == "exchange_traded_fund") {
        display_etf();
        console.log("etf");
    }
    // socket.emit("get_security_info", [info.id]);
});