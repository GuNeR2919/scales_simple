$(document).ready(function(){
    //connect to the socket server.
    const socket = io.connect('http://192.168.67.130:8000');
    // var weight_received = [];

    //receive details from server
    socket.on('weight', function(msg) {
        $('#weight').html(msg.data);
    });
});
