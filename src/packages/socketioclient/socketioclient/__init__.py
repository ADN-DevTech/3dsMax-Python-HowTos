"""
Demonstrate the use of of a socket.io client in 3dsMax
"""
import threading
import socketio
import pymxs
import mxthread

def connect_socketio():
    """Fonnect the socket io client"""
    sio = socketio.Client()

    @sio.event
    def connect():
        """Handle the connection"""
        # note: socketio calls us on a different thread.
        # 3dsMax (pymxs, the print function) don't work from a thread.
        # We use mxthread (from a different example) to execute code on
        # 3dsMax's main thread to handle the event. Note that this will
        # deadlock if the main thread is blocked (we cannot execute something
        # on the main thread if the main thread is blocked).
        mxthread.run_on_main_thread(print, "connection established")

    @sio.on("chat message")
    def my_message(data):
        """Handle a chat message"""
        mxthread.run_on_main_thread(print, f"message received {data}")
        # We could emit something here
        # sio.emit('my response', {'response': 'my response'})

        # We could disconnect ourself (so we only handle one message)
        sio.disconnect()

    @sio.event
    def disconnect():
        """Handle a disconnection"""
        mxthread.run_on_main_thread(print, "disconnected from server")

    sio.connect('http://localhost:3000')
    sio.wait()
    mxthread.run_on_main_thread(print, "no longer waiting")

x = threading.Thread(target=connect_socketio)
x.start()
