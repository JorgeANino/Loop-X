import threading
import queue
import time

class ThreadedClient(threading.Thread):
    def __init__(self, queue, fcn):
        threading.Thread.__init__(self)
        self.queue = queue
        self.fcn = fcn
    def run(self):
        time.sleep(1)
        self.queue.put(self.fcn())

