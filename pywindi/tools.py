from threading import Event, Lock

class EventManager:
    # Dictionary of events waiting to execute (event wating list).
    event_dict = {}
    lock = Lock()

    # @param timeout {Number} - the time that wait function waits for a key to send.
    def __init__(self, timeout=None):
        self.timeout = timeout

    # Fire the event in event_dict.
    #
    # @param key {String} - name of the event in the event_dict.
    def send(self, key):
        self.lock.acquire()
        if not key in self.event_dict:
            e = Event()
            self.event_dict[key] = e
        else:
            e = self.event_dict[key]
        self.lock.release()
        e.set()

    # Wait for an event in event_dict to fire.
    #
    # @param key {String} - name of the event in the event_dict.
    def wait(self, key):
        self.lock.acquire()
        if not key in self.event_dict:
            e = Event()
            self.event_dict[key] = e
        else:
            e = self.event_dict[key]
        self.lock.release()
        e.wait(self.timeout)


class Queue:
    event_manager = EventManager()
    overflow_limit = 0
    push_counter = 0
    pop_counter = 0
    queue = []

    def __init__(self, limit=50):
        self.overflow_limit = limit

    def push(self, item):
        if len(self.queue) == self.overflow_limit:
            print('Queue is full.')
            return
        self.queue.append(item)
        self.event_manager.send(self.push_counter)
        self.push_counter += 1

    def pop(self):
        self.event_manager.wait(self.pop_counter)
        self.pop_counter += 1
        item = self.queue[0]
        self.queue = self.queue[1:]
        return item
