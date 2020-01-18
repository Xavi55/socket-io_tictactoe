var socket = io();
socket.on('connect', function() {
    socket.emit('join', {username:'kevin',room:'0'});

});

socket.on('case',function(data)
{
    console.log(data)
})

document.getElementById('a').addEventListener(click,function()
{
    console.log('hi')
})