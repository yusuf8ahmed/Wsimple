var search_box = document.getElementById("search");
var socket = io("/search");

socket.on('connect', function () {
    console.log("Connected");
    socket.emit("get_search_page");
});

socket.on('invalid_token', function (data) {
    alert("Access Token is Invalid or Broken must return to login page");
    window.location.href = "/";
});

socket.on('return_search_page', function (data) {
    console.log(data);
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
    }
});