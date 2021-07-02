# HowTo: mxthread

Can a python thread queue some work to be executed by the main thread, wait for the execution
to complete and then get the result of running this code?

This question was asked on a forum. I will now try to show how this can work.


### Overview of how this can be solved

3ds Max integrates Qt and Qt provides many tools to deal with threads. The method presented
here may not be the simplest or the best but it is entirely based on Qt mechanisms.


Disclaimer: It is difficult to work with threads and even more difficult to work with
threads in 3dsMax (ex: prints are not shown in the listener window). So I would not necessarily
recommand this kind of approach. It can nevertheless be useful to adapt a library to multiple
DCCs (or other reasons). 

#### Slots and Signals
If an object that has a main thread affinity creates a slot, and that a worker 
emits a signal on this slot, the signal will be processed on the main thread. This does
not provide a way for the worker to retrieve the result of running this code.

#### QWaitCondition
A thread can wait on a QWaitCondition that another thread will raise.

#### Approach

We provide a way to bundle a function to execute in an object that is passed by a signal
to a slot that is serviced by the main thread. The bundle/payload also contains a wait
condition that the main thread raises when the payload has been executed. The return value
of the code is added to the payload so that the worker can retrieve it. Exceptions are also
propagated.

## The "test case"

To make things clearer, here is the sample program that we will use to test the maxthread
module.

We import 2 funcitons from maxthread: `on_main_thread` which allows to decorate a function
so that it will always run on the main thread, and `main_thread_print` which is an already
decorated function that prints on the main thread.

The run function of the Worker (that is a QThread) is what the worker thread does: it essentially
run stuff on the main thread.

```python
from maxthread import on_main_thread, main_thread_print
from pymxs import runtime as rt

class Worker(QThread):
    """
    Worker thread doing various things with maxtrhead.
    """
    def __init__(self, name="worker"):
        QThread.__init__(self)
        self.setObjectName(name)

    def run(self):
        # use a function that was already decorated with on_main_thread
        main_thread_print(f"hello from thread {self.objectName()}")
     
        # create our own function decorated with on_main_thread
        @on_main_thread
        def do_pymxs_stuff():
            print("resetting the max file")
            # reset the max file (so that the scene is empty)
            rt.resetMaxFile(rt.name("noprompt"))            
            # we are on main thread so we can use print and it will work
            print("creating 3 boxes on main thread")
            # pymxs stuff can only work on the main thread. Well no problem we are on the main thread:
            rt.box(width=1, height=1, depth=1, position=rt.Point3(0,0,0))
            rt.box(width=1, height=1, depth=1, position=rt.Point3(0,0,2))
            rt.box(width=1, height=1, depth=1, position=rt.Point3(0,0,4))
            
            # make 3ds Max aware that the views are dirtied
            rt.redrawViews()
            
            return 3
        # call our main thread function 
        res = do_pymxs_stuff()
        main_thread_print(f"our main thread function returned {res}")

        # create another function that will throw something
        # (to show that exceptions are propagated)
        @on_main_thread
        def do_faulty_stuff():
            # we are on main thread so we can use print and it will work
            a = 2
            b = 0
            return a / b
        try:
            res = do_faulty_stuff()
            main_thread_print(f"The function will fail, this will never be displayed")
        except Exception as e:
            main_thread_print(f"our main thread function raised:  {e}")


        # use a lambda instead
        on_main_thread(lambda : print("hello from lambda"))()


# Name the main thread
QThread.currentThread().setObjectName("main_thread")
# create a worker
worker = Worker("worker_thread")
worker.start()
# Note: we cannot wait this worker here. This will create a deadlock.
# The worker executes stuff on the main thread and we are on the main thread.
# But to convince ourselves, we can print something here and the man thread
# calls initiated by the worker will all happen after this
print("--- Worker thread calls to the main thread will run after this")
```

## How to use it

To create a function that will be executed on the main thread (no matter what thread calls the function),
the function needs to be decorated with `@on_main_thread`, as shown here:

```
@on_main_thread
def do_faulty_stuff():
    # we are on main thread so we can use print and it will work
    a = 2
    b = 0
    return a / b
```

Decorated functions can return values and throw exceptions and in both cases this
behaves normally from the thread that calls the function.

### gotcha

The most important gotcha is that the main thread cannot wait for its worker (this
will create a deadlock). The worker should also be kept in a variable until it completes.

## The implementation

The implementation of mxthread can be found in [mxtrhead/__init__.py](mxthread/__init__.py).
The code is abundantly commented.

- `on_main_thread` is a decorator that makes a function runnable on the main thread

- `main_thread_print` is a function that uses `on_main_thread` to make the main thread print
something (in 3dsMax print does not work from a worker thread)

- RunnableWaitablePayload is an object that is passed by a worker thread using the `RUNNABLE_PAYLOAD_SIGNAL`
to the `RUNNABLE_PAYLOAD_SLOT` that runs on the main thread. This payload object contains
the function that needs to be called on the main thread. After the function runs it contains
the return value of the function or an exception if an exception was raised. It also contains
a QWaitCondition. The caller worker waits for this QWaitCondition and the main thread triggers
it when the function has been executed.


