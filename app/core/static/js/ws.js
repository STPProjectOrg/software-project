    var loc = window.location
    var wsStart = "ws://"
    if (loc.protocol == "https:"){
        wsStart = "wss://"
    }
    var webSocketEndpoint =  wsStart + loc.host + '/notifications/ddd7s/'  // ws : wss   // Websocket URL, Same on as mentioned in the routing.py


    var socket = new WebSocket(webSocketEndpoint) // Creating a new Web Socket Connection

    // Socket On receive message Functionality
    socket.onmessage = function(e){
        console.log('message', e)
        console.log(e.data) // Access the notification data
        //$("body").append("<h3>"+e.data+"</h3>")
        // Can write any functionality based on your requirement
    }

    // Socket Connet Functionality
    socket.onopen = function(e){
        console.log('open', e)
    }

    // Socket Error Functionality
    socket.onerror = function(e){
        console.log('error', e)
    }

    // Socket close Functionality
    socket.onclose = function(e){
        console.log('closed', e)
    }