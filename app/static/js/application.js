$(document).ready(function(){
    //connect to the socket server.
    const socket = io.connect('http://' + location.hostname + ':' + location.port);
    // var weight_received = [];

    //receive details from server
    socket.on('weight', function(msg) {
        $('#weight').html(msg.data);
    });
});
