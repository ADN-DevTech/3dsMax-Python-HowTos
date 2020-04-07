'''
   Demonstrates the use of mxstoken
'''
import threading
import time
import pymxs # pylint: disable=import-error

def mxstoken_sample():
    '''
    Demonstrate 3 threads using mxstoken.
    '''
    flag = True
    counter = 0

    def call_mxs_entry():
        '''
        Access pymxs in a mxstoken protected block of code.
        '''
        with pymxs.mxstoken():
            pymxs.runtime.Teapot()

    def call_mxs_entry_ex_1(locker, tick, evt):
        '''
        Demonstrate a first function with a mix of concurrent code 
        and mxstoken protected code.
        '''
        try:
            locker.acquire()
            nonlocal flag, counter
            flag = False
            with pymxs.mxstoken():
                pymxs.runtime.Teapot(Name="call_mxs_entry_ex_1")
                # give up lock, let ex_2 could exec codes
                locker.release()
                if not evt.wait(tick):
                    pymxs.print_(
                        "Error: event untriggered\n" +
                        "which indicates 'with block' in ex_2 haven't finished\n",
                        True,
                        True)
                counter = 30
        except:
            pymxs.print_("Error: unexpected exception\n", True, True)
            raise
        finally:
            if locker.locked():
                locker.release()

    def call_mxs_entry_ex_2(locker, tick, evt):
        '''
        Demonstrate a second function with a mix of concurrent code 
        and mxstoken protected code.
        '''
        nonlocal flag, counter
        while flag:
            time.sleep(tick)

        try:
            locker.acquire()
            # we expected this block is finished
            # before ex_1 wakeup from sleep
            for _ in range(10):
                # only a indicator, could just assign counter = 10
                counter = counter + 1
            evt.set()
            with pymxs.mxstoken():
                # this block won't be executed after ex_1 with block finished
                pymxs.runtime.Teapot(Name="call_mxs_entry_ex_2")
                if counter != 30:
                    pymxs.print_(
                        ("Error: expected counter 30, got %d" +
                         "which indicates 'with block' in ex_2 haven't finished\n").format(counter),
                        True,
                        True)
        finally:
            if locker.locked():
                locker.release()
        pymxs.print_("success\n", False, True)

    # Steps:
    locker = threading.Lock()
    evt = threading.Event()
    thread1 = threading.Thread(target=call_mxs_entry)
    thread2 = threading.Thread(target=call_mxs_entry_ex_1, args=(locker, 1, evt))
    thread3 = threading.Thread(target=call_mxs_entry_ex_2, args=(locker, 0.01, evt))
    thread1.start()
    thread2.start()
    thread3.start()

mxstoken_sample()
