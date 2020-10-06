var socket = io("/settings");

socket.on('invalid_token', function (data) {
    alert("Access Token is Invalid or Broken must return to login page");
    window.location.href = "/";
});

socket.on('connect', function () {
    console.log("connected");
    socket.emit("get_settings", []);
});

socket.on('return_settings', function (data) {
    console.dir(data);
});