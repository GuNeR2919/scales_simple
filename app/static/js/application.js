$(document).ready(function(){
    //connect to the socket server.
    const socket = io.connect('http://' + location.hostname + ':' + location.port);
    // var weight_received = [];

    //receive details from server
    socket.on('weight', function(msg) {
        $('#weight').html(msg.data);
    });

    // handle socket disconnect event
    socket.on('disconnect', function(){
        console.log('Socket connection closed.');
        $('#weight').html("Connecting to scales...");
    });

    // handle socket errors
    socket.on('error', function(error){
        console.error('Socket error:', error);
        $('#weight').html("Connecting to scales...");
    });
});
