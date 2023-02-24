"""
    Provide a way to decorate python functions so that they are always executed in
    the main thread of 3dsMax. The functions can throw exceptions and return values
    and this is propagated to the caller in the thread.
"""
import sys
import os
import functools
from PySide2.QtCore import QObject, Slot, Signal, QThread, QMutex, QWaitCondition, QTimer
from PySide2.QtWidgets import QApplication
#pylint: disable=W0703,R0903,useless-option-value,R0201

class RunnableWaitablePayload():
    """
    Wrap a function call as a payload that will be emitted
    to a slot owned by the main thread. The main thread will execute
    the function call and package the return value in the payload.
    The payload also contains a wait condition that the main thread will
    signal when the payload was executed. The worker thread (that creates
    the payload) will wait for this wait condition and then retrieve the
    return value from the function.
    """
    def __init__(self, todo):
        """
        Initialize the payload.
        todo is the function to execute, that takes no arguments but
        that can return a value.
        """
        self.todo = todo
        self.todo_exception = None
        self.todo_return_value = None
        self.wcnd = QWaitCondition()
        self.mutex = QMutex()

    def wait_for_todo_function_to_complete_on_main_thread(self):
        """
        Wait for the pending operation to complete
        Returns the value returned by the todo function (the function
        to execute in this payload).
        """
        self.mutex.lock()
        # queue the thing to do on the main thread
        RUNNABLE_PAYLOAD_SIGNAL.sig.emit(self)
        # while waiting the QWaitCondition unlocks the mutex
        # and relocks it when the wait completes
        self.wcnd.wait(self.mutex)
        self.mutex.unlock()
        # if the payload failed, propagate this to the thread
        if self.todo_exception:
            raise self.todo_exception
        # otherwise return the result
        return self.todo_return_value

    def run_todo_function(self):
        """
        Run the todo function of payload.
        This will add the return of the todo function to the payload as "todo_return_value".
        """
        self.mutex.lock()
        try:
            self.todo_return_value = self.todo()
        except Exception as exception:
            self.todo_exception = exception
        self.wcnd.wakeAll()
        self.mutex.unlock()

class RunnableWaitablePayloadSignal(QObject):
    """
    Creates a signal that can be used to send RunnableWaitablePyaloads to
    the main thread for execution.
    """
    sig = Signal(RunnableWaitablePayload)

# Create the Slots that will receive signals
class PayloadSlot(QObject):
    """
    Slot for function submission on the main thread.
    """
    def __init__(self):
        """
        An object that owns a slot.
        This object's affinity is the main thread so that signals it receives
        will run on the main thread.
        """
        QObject.__init__(self)
        self.moveToThread(QApplication.instance().thread())

    @Slot(RunnableWaitablePayload)
    def run(self, ttd):
        """
        Run the slot payload.
        """
        ttd.run_todo_function()

RUNNABLE_PAYLOAD_SLOT = PayloadSlot()

# connect the payload signal to the payload slot
RUNNABLE_PAYLOAD_SIGNAL = RunnableWaitablePayloadSignal()
RUNNABLE_PAYLOAD_SIGNAL.sig.connect(RUNNABLE_PAYLOAD_SLOT.run)

def run_on_main_thread(todo, *args, **kwargs):
    """
    Run code on the main thread.
    Returns the return value of the todo code. If this is called
    from the main thread, todo is immediately called.
    """
    if QThread.currentThread() is QApplication.instance().thread():
        return todo(*args, **kwargs)
    ttd = RunnableWaitablePayload(lambda: todo(*args, **kwargs))
    return ttd.wait_for_todo_function_to_complete_on_main_thread()

def on_main_thread(func):
    """
    Decorate a function to make it always run on the main thread.
    """
    # preserve docstring of the wrapped function
    @functools.wraps(func)
    def decorated(*args, **kwargs):
        return run_on_main_thread(func, *args, **kwargs)
    return decorated

@on_main_thread
def main_thread_print(*args, **kwargs):
    """
    Print on the main thread.
    """
    return print(*args, **kwargs)
