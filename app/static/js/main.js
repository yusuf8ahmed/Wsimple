var toggle_price_to_shares = false; // show current price auto
var data_cache = {};
const updated_on = document.getElementById("updated_on");
var checkbox_price_shares = document.getElementById("checkbox_price_shares");
var available_to_trade = document.getElementById("available_to_trade");
var account_value = document.getElementById("account_value");
var net_deposits = document.getElementById("net_deposits");
var available_to_withdraw = document.getElementById("available_to_withdraw");
var account_positions_box = document.getElementById("account_positions_box");
var account_watchlist_box = document.getElementById("account_watchlist_box");
var account_change = document.getElementById("account_change");
const ctx = document.getElementById('chart').getContext('2d');

var gradient = ctx.createLinearGradient(0, 0, 0, 350);
gradient.addColorStop(0, 'rgba(250, 177, 50,1)');
gradient.addColorStop(1, 'rgba(250, 174, 50,0)');

var socket = io("/dashboard", {transports: ['websocket'], upgrade: false});

function price_to_shares() {
    console.log(checkbox_price_shares.checked);
    account_positions_box.innerHTML = '';
    for (const positions of data_cache.account_positions.table.results) {
        var pposition_div = document.createElement("div");
        pposition_div.style.margin = "2px 0px";
        pposition_div.style.display = "flex";
        pposition_div.style.justifyContent = "space-between";
        // securities symbol and link
        var pposition_symbol = document.createElement("p");
        pposition_symbol.style.margin = "0px";
        var pposition_symbol_link = document.createElement("a");
        pposition_symbol_link.setAttribute("target", "_blank");
        pposition_symbol_link.setAttribute("href", `${window.location.origin}/search/${positions.id}`);
        var position_symbol_text = document.createTextNode(positions.stock.symbol);
        pposition_symbol_link.appendChild(position_symbol_text);
        // securities value
        var pposition_value = document.createElement("p");
        pposition_value.style.margin = "0px"; 
        var position_value;  
        if (checkbox_price_shares.checked) {
            // display shares held true
            toggle_price_to_shares = true;
            position_value = document.createTextNode(`${positions.quantity}`);
            console.log("shares held");
        } else {
            // display current price of positions false    
            toggle_price_to_shares = false; 
            position_value = document.createTextNode(`${parseFloat(positions.quote.amount).toFixed(2)} ${positions.quote.currency}`);    
            console.log("current price");
        }
        // attaching elements
        pposition_symbol.appendChild(pposition_symbol_link);
        pposition_div.appendChild(pposition_symbol);
        pposition_value.appendChild(position_value);
        pposition_div.appendChild(pposition_value);
        account_positions_box.appendChild(pposition_div);
    }
}

updated_on.appendChild(document.createTextNode(`S/${new Date().toLocaleTimeString()}`));

socket.on('connect', function () {
    console.log("socket.io connected");
    socket.emit('dashboard');
    console.log("emitted to dashboard");
});

socket.on('invalid_token', function (data) {
    alert("Access Token is Invalid or Broken must return to login page");
    window.location.href = "/";
});

socket.on('main_dashboard_info', function (data) {
    updated_on.innerHTML = "";
    updated_on.appendChild(document.createTextNode(`U/${new Date().toLocaleTimeString()}`));
    console.log(`updated ${ data.account_value_graph.table.length } ${ new Date().toLocaleTimeString() }`);
    data_cache = null;  data_cache = data;
    account_positions_box.innerHTML = '';
    account_watchlist_box.innerHTML = '';
    let account_value_list = [];
    let account_net_deposit_list = [];
    let account_label = [];

    var chart = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [{
                label: "account value",
                backgroundColor: gradient,
                borderColor: "#FAB132",
                strokeColor: "#FAB132",
                pointColor: "#FAB132",
                pointStrokeColor: "#FAB132",
                pointHighlightFill: "#FAB132",
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
                    gridLines: { display: false }
                }],
                yAxes: [{
                    gridLines: { display: false },
                    ticks: { callback: function(value) {if (value % 1 === 0) {return value;}} }
                }]
            }
        }
    });

    for (const account_value of data.account_value_graph.table) {
        var date = new Date(account_value.date);
        chart.data.labels.push(date.toLocaleTimeString([], {
            timeStyle: 'short'
        }));
        chart.data.datasets.forEach((dataset) => {
            dataset.data.push(account_value.value.amount.toFixed(2));
        });
        chart.update();
    }

    console.log(data);

    for (const positions of data.account_positions.table.results) {
        var pposition_div = document.createElement("div");
        pposition_div.style.margin = "2px 0px";
        pposition_div.style.display = "flex";
        pposition_div.style.justifyContent = "space-between";
        // securities symbol and link
        var pposition_symbol = document.createElement("p");
        pposition_symbol.style.margin = "0px";
        var pposition_symbol_link = document.createElement("a");
        pposition_symbol_link.setAttribute("target", "_blank");
        pposition_symbol_link.setAttribute("href", `${window.location.origin}/search/${positions.id}`);
        var position_symbol_text = document.createTextNode(positions.stock.symbol);
        pposition_symbol_link.appendChild(position_symbol_text);
        // securities value
        var pposition_value = document.createElement("p");
        pposition_value.style.margin = "0px"; 
        var position_value;        
        if (toggle_price_to_shares) {
            position_value = document.createTextNode(`${positions.quantity}`);
        } else {
            position_value = document.createTextNode(`${parseFloat(positions.quote.amount).toFixed(2)} ${positions.quote.currency}`);            
        }
        // attaching elements
        pposition_symbol.appendChild(pposition_symbol_link);
        pposition_div.appendChild(pposition_symbol);
        pposition_value.appendChild(position_value);
        pposition_div.appendChild(pposition_value);
        account_positions_box.appendChild(pposition_div);
    }

    account_value.innerHTML = `
    Account value: ${data.account_value.amount.toFixed(2)} ${data.account_value.currency}
    `;    
    account_change.innerHTML = `
    Account change: $${data.account_change.amount}(${data.account_change.percentage}%)
    `;    
    net_deposits.innerHTML = `
    Net deposit: ${data.net_deposits.amount} ${data.net_deposits.currency}
    `;    
    available_to_trade.innerHTML = `
    Available to trade: ${data.available_to_trade.amount} ${data.available_to_trade.currency}
    `;
    available_to_withdraw.innerHTML = `
    Available to withdraw: ${data.available_to_withdraw.amount} ${data.available_to_withdraw.currency}
    `;


    for (const watchlist of data.account_watchlist.table.securities) {
        var pwatchlist_div = document.createElement("div");
        pwatchlist_div.style.margin = "2px 0px";
        pwatchlist_div.style.display = "flex";
        pwatchlist_div.style.justifyContent = "space-between";
        // securities symbol
        var pwatchlist_symbol = document.createElement("p");
        pwatchlist_symbol.style.margin = "0px";
        var pwatchlist_symbol_link = document.createElement("a");
        pwatchlist_symbol_link.setAttribute("target", "_blank");
        pwatchlist_symbol_link.setAttribute("href", `${window.location.origin}/search/${watchlist.id}`);
        var pwatchlist_symbol_text = document.createTextNode(watchlist.stock.symbol);
        pwatchlist_symbol_link.appendChild(pwatchlist_symbol_text);
        // securities value
        var pwatchlist_value = document.createElement("p");
        pwatchlist_value.style.margin = "0px";
        // pwatchlist_value.style.cssFloat = "right";
        var value = document.createTextNode(`${parseFloat(watchlist.quote.amount).toFixed(2)} ${watchlist.quote.currency}`);
        // attaching elements
        pwatchlist_symbol.appendChild(pwatchlist_symbol_link);
        pwatchlist_div.appendChild(pwatchlist_symbol);
        pwatchlist_value.appendChild(value);
        pwatchlist_div.appendChild(pwatchlist_value);
        account_watchlist_box.appendChild(pwatchlist_div);
    }
});