var search_box = document.getElementById("search");
var top_losers_list = document.getElementById("top-losers-list");
var top_gainers_list = document.getElementById("top-gainers-list");
var most_active_list = document.getElementById("most-active-list");
var most_watched_list = document.getElementById("most-watched-list");
var socket = io("/search");

socket.on('connect', function () {
    console.log("socket.io connected");
    socket.emit("get_search_page");
    console.log("emitted to dashboard");
});

socket.on('invalid_token', function (data) {
    alert("Access Token is Invalid or Broken must return to login page");
    window.location.href = "/";
});

function clear_all_lists() {
    top_losers_list.innerHTML = "";
    top_gainers_list.innerHTML = "";
    most_active_list.innerHTML = "";
    most_watched_list.innerHTML = "";
}

function update_top_losers(data) {
    for (const item of data) {
        var icon_i = document.createElement("i");
        icon_i.setAttribute("class", "material-icons");  
        icon_i.innerHTML = "send";   
        var icon_a = document.createElement("a"); 
        icon_a.setAttribute("href", "#!"); 
        icon_a.setAttribute("class", "secondary-content");  
        icon_a.appendChild(icon_i)
        var inner_div = document.createElement("div");
        var inner_div_symbol = document.createTextNode(item.symbol)
        inner_div.appendChild(inner_div_symbol)
        inner_div.appendChild(icon_a)
        var parent_li = document.createElement("li");
        parent_li.setAttribute("class","collection-item")
        parent_li.appendChild(inner_div)
        top_losers_list.appendChild(parent_li)
    }
}

function update_top_gainers(data) {
    for (const item of data) {
        var icon_i = document.createElement("i");
        icon_i.setAttribute("class", "material-icons");  
        icon_i.innerHTML = "send";   
        var icon_a = document.createElement("a"); 
        icon_a.setAttribute("href", "#!"); 
        icon_a.setAttribute("class", "secondary-content");  
        icon_a.appendChild(icon_i)
        var inner_div = document.createElement("div");
        var inner_div_symbol = document.createTextNode(item.symbol)
        inner_div.appendChild(inner_div_symbol)
        inner_div.appendChild(icon_a)
        var parent_li = document.createElement("li");
        parent_li.setAttribute("class","collection-item")
        parent_li.appendChild(inner_div)
        top_gainers_list.appendChild(parent_li)
    }
}

function update_most_active(data) {
    for (const item of data) {
        var icon_i = document.createElement("i");
        icon_i.setAttribute("class", "material-icons");  
        icon_i.innerHTML = "send";   
        var icon_a = document.createElement("a"); 
        icon_a.setAttribute("href", "#!"); 
        icon_a.setAttribute("class", "secondary-content");  
        icon_a.appendChild(icon_i)
        var inner_div = document.createElement("div");
        var inner_div_symbol = document.createTextNode(item.symbol)
        inner_div.appendChild(inner_div_symbol)
        inner_div.appendChild(icon_a)
        var parent_li = document.createElement("li");
        parent_li.setAttribute("class","collection-item")
        parent_li.appendChild(inner_div)
        most_active_list.appendChild(parent_li)
    }
}

function update_most_watched(data) {
    for (const item of data) {
        var icon_i = document.createElement("i");
        icon_i.setAttribute("class", "material-icons");  
        icon_i.innerHTML = "send";   
        var icon_a = document.createElement("a"); 
        icon_a.setAttribute("href", "#!"); 
        icon_a.setAttribute("class", "secondary-content");  
        icon_a.appendChild(icon_i)
        var inner_div = document.createElement("div");
        var inner_div_symbol = document.createTextNode(item.stock.symbol)
        inner_div.appendChild(inner_div_symbol)
        inner_div.appendChild(icon_a)
        var parent_li = document.createElement("li");
        parent_li.setAttribute("class","collection-item")
        parent_li.appendChild(inner_div)
        most_watched_list.appendChild(parent_li)
    }
}

socket.on('return_search_page', function (data) {
    console.log(data);
    clear_all_lists()
    update_top_losers(data.top_losers.results)
    update_top_gainers(data.top_gainers.results)
    update_most_active(data.most_active.results)
    update_most_watched(data.most_watched.results)
});

socket.on('return_security', function (data) {
    // width: 40vw; height: auto; border: none; background: #ffffff; border-radius: 23px;
    search_box.innerHTML = '';
    // console.dir(data[0].results);
    for (const securities of data[0].results) {
        var security = document.createElement("p");
        var security_box = document.createElement("a");
        security_box.setAttribute("target", "_blank");
        security_box.setAttribute("href", `${window.location.origin}/search/${securities.id}`);
        security_box.innerHTML = `${securities.stock.symbol}`;
        security.appendChild(security_box);
        search_box.appendChild(security);
    }
});

const addfriend = document.getElementById("query");
addfriend.addEventListener('input', function (e) {
    console.log("search for security", e.target.value);
    if (!(e.target.value === '' || e.target.value === ' ')) {
        socket.emit("find_security", [e.target.value]); 
    } else {
        console.log("unable to search for a ticker with space?")
        search_box.innerHTML = '';
    }
});