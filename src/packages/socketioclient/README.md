# HowTo: socketioclient

This example shows how to connect to a socket.io server from 3dsMax.

The sample uses the following PyPi pacakges: 

- `python-socketio` the socketio support for python
- `websocket-client` the websocket client for socketio

It also uses the following package (from another sample in this repo): `mxtread` 


The code of this sample is very concise and two things are important to
know:

## socketio events are not handled on the main thread

This handler is not called on the main thread:

```python
    @sio.on("chat message")
    def my_message(data):
        mxthread.run_on_main_thread(print, f"message received {data}")
        # We could emit something here
        # sio.emit('my response', {'response': 'my response'})

        # We could disconnect ourself (so we only handle one message)
        sio.disconnect()
```

But 3dsMax will not print on separate threads and none of the pymxs
functions (and properties) can be used on a thread (other than the
main thread).


This is why we use mxthread. This module lets "execute code on the main
thread". So here we call print on the main thread. We could write our own
custom function that does various things with pymxs and call it on the main
thread here. As long as the main thread itself is not blocked this will work.

## you typically call sio.wait() on the socket io client

This, if called on the main thread, blocks the main thread (this will
freeze the 3dsMax ui as long as sio.wait does not return). So we create
the socket io client from a subthread.

```python
x = threading.Thread(target=connect_socketio)
x.start()
```
## Server code

We need a nodejs server (using express and socket.io) to run the sample.
We pretty much use the [chat](https://socket.io/get-started/chat) sample provided on the socket.io site.

You will need to install nodejs and express to make that work. You can
follow the instructions provided on the socket.io

- index.html
```html
<!DOCTYPE html>
<html>
  <head>
    <title>Socket.IO chat</title>
    <style>
      body { margin: 0; padding-bottom: 3rem; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }

      #form { background: rgba(0, 0, 0, 0.15); padding: 0.25rem; position: fixed; bottom: 0; left: 0; right: 0; display: flex; height: 3rem; box-sizing: border-box; backdrop-filter: blur(10px); }
      #input { border: none; padding: 0 1rem; flex-grow: 1; border-radius: 2rem; margin: 0.25rem; }
      #input:focus { outline: none; }
      #form > button { background: #333; border: none; padding: 0 1rem; margin: 0.25rem; border-radius: 3px; outline: none; color: #fff; }

      #messages { list-style-type: none; margin: 0; padding: 0; }
      #messages > li { padding: 0.5rem 1rem; }
      #messages > li:nth-child(odd) { background: #efefef; }
    </style>
  </head>
  <body>
    <ul id="messages"></ul>
    <form id="form" action="">
      <input id="input" autocomplete="off" /><button>Send</button>
    </form>
    <script src="/socket.io/socket.io.js"></script>

    <script>
      var socket = io();

      var messages = document.getElementById('messages');
      var form = document.getElementById('form');
      var input = document.getElementById('input');

      form.addEventListener('submit', function(e) {
        e.preventDefault();
        if (input.value) {
          socket.emit('chat message', input.value);
          input.value = '';
        }
      });

      socket.on('chat message', function(msg) {
        var item = document.createElement('li');
        item.textContent = msg;
        messages.appendChild(item);
        window.scrollTo(0, document.body.scrollHeight);
      });
    </script>
  </body>
</html>
```

- index.js

The code is here:
```javascript
const app = require('express')();
const http = require('http').Server(app);
const io = require('socket.io')(http);
const port = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

io.on('connection', (socket) => {
  console.log('a user connected');
  socket.on('disconnect', () => {
    console.log('user disconnected');
  });
  socket.on('chat message', msg => {
    io.emit('chat message', msg);
  });
});

http.listen(port, () => {
  console.log(`Socket.IO server running at http://localhost:${port}/`);
});
```

- package.json

You will also need the package.json file:

```json
{
  "name": "socket-chat-example",
  "version": "0.0.1",
  "description": "my first socket.io app",
  "dependencies": {
    "express": "^4.17.3",
    "socket.io": "^4.4.1"
  }
}
```

### Installing the server
npm install

### Running the server
node index.js

### Running the max sample
When the serever run you can point your browser to localhost:3000 and
type some stuff.

You can then import socketioclient from the python console in max and.
After it is imported (the code automatically calls sio.disconnect after
the first message is received) you will be able to see events printed
on the console.
