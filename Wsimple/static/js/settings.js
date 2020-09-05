var socket = io();

socket.on('connect', function () {
    console.log("connected");
    socket.emit("get_settings", []);
});

socket.on('return_settings', function (data) {
    console.dir(data);
});