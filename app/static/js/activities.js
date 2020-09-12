var activities_box = document.getElementById("activities_box");
var color_int = 0;
var bookmark;

var socket = io("/activities",{
    transports: ['websocket']
  });

socket.on('connect', function () {
    console.log("socket.io connected");
    socket.emit('get_activities', []);
});

function display_buys(pposition_div, activities) {
    // securities symbol
    var pposition_symbol = document.createElement("p");
    pposition_symbol.style.margin = "0px";
    var pposition_symbol_link = document.createElement("a");
    pposition_symbol_link.style.fontSize = "1.2rem";
    var position_symbol_text = document.createTextNode(`${activities.object} ${activities.order_type} ${activities.order_sub_type}`);
    pposition_symbol_link.appendChild(position_symbol_text);
    // securities value
    var pposition_value = document.createElement("p");
    pposition_value.style.margin = "0px";
    var position_value;
    if (activities.status == "cancelled") {
        position_value = document.createTextNode("Cancelled"); 
    } else if (activities.status == "posted") {
        position_value = document.createTextNode(`${activities.symbol} ${activities.quantity} ${activities.market_value.amount.toFixed(2)} ${activities.market_value.currency}`); 
    } else if (activities.status == "expired") {
        position_value = document.createTextNode("Expired"); 
    } else {
        position_value = document.createTextNode("None"); 
    }
    // attaching elements
    pposition_symbol.appendChild(pposition_symbol_link);
    pposition_div.appendChild(pposition_symbol);
    pposition_value.appendChild(position_value);
    pposition_div.appendChild(pposition_value);
    activities_box.appendChild(pposition_div);
}
function display_sells(pposition_div, activities) {
    // securities symbol
    var pposition_symbol = document.createElement("p");
    pposition_symbol.style.margin = "0px";
    var pposition_symbol_link = document.createElement("a");
    pposition_symbol_link.style.fontSize = "1.2rem";
    var position_symbol_text = document.createTextNode(`${activities.object} ${activities.order_type} ${activities.order_sub_type}`);
    pposition_symbol_link.appendChild(position_symbol_text);
    // securities value
    var pposition_value = document.createElement("p");
    pposition_value.style.margin = "0px";
    var position_value;
    if (activities.status == "cancelled") {
        position_value = document.createTextNode("Cancelled"); 
    } else if (activities.status == "posted") {
        position_value = document.createTextNode(`${activities.market_value.amount.toFixed(2)} ${activities.market_value.currency}`); 
    } else if (activities.status == "expired") {
        position_value = document.createTextNode("Expired"); 
    } else {
        position_value = document.createTextNode("None"); 
    }
    // attaching elements
    pposition_symbol.appendChild(pposition_symbol_link);
    pposition_div.appendChild(pposition_symbol);
    pposition_value.appendChild(position_value);
    pposition_div.appendChild(pposition_value);
    activities_box.appendChild(pposition_div);
}
function display_deposits(pposition_div, activities) {
    // securities symbol
    var pposition_symbol = document.createElement("p");
    pposition_symbol.style.margin = "0px";
    var pposition_symbol_link = document.createElement("a");
    pposition_symbol_link.style.fontSize = "1.2rem";
    var position_symbol_text = document.createTextNode(activities.object);
    pposition_symbol_link.appendChild(position_symbol_text);
    // securities value
    var pposition_value = document.createElement("p");
    pposition_value.style.margin = "0px";
    var position_value;
    if (activities.status == "cancelled") {
        position_value = document.createTextNode("Cancelled"); 
    } else if (activities.status == "accepted") {
        position_value = document.createTextNode(`${activities.value.amount.toFixed(2)} ${activities.value.currency}`); 
    } else {
        position_value = document.createTextNode("None"); 
    }
    // attaching elements
    pposition_symbol.appendChild(pposition_symbol_link);
    pposition_div.appendChild(pposition_symbol);
    pposition_value.appendChild(position_value);
    pposition_div.appendChild(pposition_value);
    activities_box.appendChild(pposition_div);
}
function display_withdrawals(pposition_div, activities) {
    // securities symbol
    var pposition_symbol = document.createElement("p");
    pposition_symbol.style.margin = "0px";
    var pposition_symbol_link = document.createElement("a");
    pposition_symbol_link.style.fontSize = "1.2rem";
    var position_symbol_text = document.createTextNode(activities.object);
    pposition_symbol_link.appendChild(position_symbol_text);
    // securities value
    var pposition_value = document.createElement("p");
    pposition_value.style.margin = "0px";
    var position_value;
    if (activities.status == "cancelled") {
        position_value = document.createTextNode("Cancelled"); 
    } else if (activities.status == "accepted") {
        position_value = document.createTextNode(`${activities.value.amount.toFixed(2)} ${activities.value.currency}`); 
    } else {
        position_value = document.createTextNode("None"); 
    }
    // attaching elements
    pposition_symbol.appendChild(pposition_symbol_link);
    pposition_div.appendChild(pposition_symbol);
    pposition_value.appendChild(position_value);
    pposition_div.appendChild(pposition_value);
    activities_box.appendChild(pposition_div);
}
function display_dividends(pposition_div, activities) {
    // securities symbol
    var pposition_symbol = document.createElement("p");
    pposition_symbol.style.margin = "0px";
    var pposition_symbol_link = document.createElement("a");
    pposition_symbol_link.style.fontSize = "1.2rem";
    var position_symbol_text = document.createTextNode(activities.object);
    pposition_symbol_link.appendChild(position_symbol_text);
    // securities value
    var pposition_value = document.createElement("p");
    pposition_value.style.margin = "0px";
    var position_value = document.createTextNode(`${activities.process_date} ${activities.symbol} ${activities.market_value.amount.toFixed(2)} ${activities.market_value.currency}`); 
    // attaching elements
    pposition_symbol.appendChild(pposition_symbol_link);
    pposition_div.appendChild(pposition_symbol);
    pposition_value.appendChild(position_value);
    pposition_div.appendChild(pposition_value);
    activities_box.appendChild(pposition_div);
}

// activity type unknown below
function display_account_transfer(pposition_div, activities) {
    console.log("account transfer activity type unknown");
}
function display_refunds(pposition_div, activities) {
    console.log("refunds activity type unknown");
}
function display_referral_rewards(pposition_div, activities) {
    console.log("referral rewards activity type");
}

socket.on('display_activities', function (data) {
    bookmark = data.bookmark;
    console.dir(data);
    for (const activities of data.results) {
        var pposition_div = document.createElement("div");
        pposition_div.style.padding = "9px 9px";
        pposition_div.style.display = "flex";
        pposition_div.style.justifyContent = "space-between";
        if ((color_int % 2) == 0) {
            // pposition_div.style.backgroundColor = "#DCDCDC";
            pposition_div.style.borderTop = "3px solid #FAB132";
            pposition_div.style.borderBottom = "3px solid #FAB132";
        } else {
            pposition_div.style.backgroundColor = "transparent";
        }

        if (activities.object == "order" && activities.order_type == "buy_quantity") {
            display_buys(pposition_div, activities);
        } else if (activities.object == "order" && activities.order_type == "sell_quantity") {
            display_sells(pposition_div, activities);
        } else if (activities.object == "deposit") {
            display_deposits(pposition_div, activities);
        } else if (activities.object == "withdrawal") {
            display_withdrawals(pposition_div, activities);
        } else if (activities.object == "dividend") {
            display_dividends(pposition_div, activities);
        } else {
            alert("open javascript console");
            console.error(`unknown wealthsimple activity type ${activities.object}`);
        }
        color_int++;
    }
    color_int = 0;
});

activities_box.onscroll = function (elem) {
    // console.log(`scrollng update ${activities_box.scrollTop} ${activities_box.scrollHeight} ${activities_box.offsetHeight}`);
    if ( (activities_box.scrollHeight == (activities_box.scrollTop + activities_box.offsetHeight))) {
        // prevent duplicate bookmarks being sent
        console.log("scrollng update true");
        socket.emit('get_activities', [bookmark]);
        elem.scrollTop = elem.scrollHeight;
    }
};