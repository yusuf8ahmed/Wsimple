var activities_box = document.getElementById("activities_box");
var bookmark;

var socket = io();

socket.on('connect', function () {
    console.log("socket.io connected");
    socket.emit('get_activities', []);
});

socket.on('display_activities', function (data) {
    bookmark = data.bookmark;
    console.dir(data);
    for (const activities of data.results) {
        var pposition_div = document.createElement("div");
        pposition_div.style.margin = "9px 9px";
        pposition_div.style.display = "flex";
        pposition_div.style.backgroundColor = "transparent";
        pposition_div.style.justifyContent = "space-between";
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
        var position_value = document.createTextNode("");
        // attaching elements
        pposition_symbol.appendChild(pposition_symbol_link);
        pposition_div.appendChild(pposition_symbol);
        pposition_value.appendChild(position_value);
        pposition_div.appendChild(pposition_value);
        activities_box.appendChild(pposition_div);
    }
});

activities_box.onscroll = function (elem) {
    console.log(`scrollng update ${activities_box.scrollTop} ${activities_box.scrollHeight} ${activities_box.offsetHeight}`);
    if (activities_box.scrollHeight == (activities_box.scrollTop + activities_box.offsetHeight)) {
        console.log("scrollng update true");
        socket.emit('get_activities', [bookmark]);
        elem.scrollTop = elem.scrollHeight;
    }
};