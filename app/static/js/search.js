var search_box = document.getElementById("search");
var socket = io();

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
    if (e.target.value === '') {
        socket.emit("find_security", [""]);
    } else {
        socket.emit("find_security", [e.target.value]);
    }
});