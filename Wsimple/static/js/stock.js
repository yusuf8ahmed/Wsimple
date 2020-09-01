var socket = io();

socket.on('connect', function () {
    console.log("connected");
    var sec_id = window.location.pathname;
    socket.emit("get_security_info", [sec_id.split("/")[2]]);
});

socket.on('return_stock_info', function (data) {
    console.log("return stock search");
    console.dir(data);
    socket.emit("get_security_info", [data[1].id]);
});

// window.onbeforeunload = function() {
//     console.log("beforeunload");
//     socket.disconnect();
// }