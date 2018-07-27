from threading import Event, Lock

class EventManager:
    # Dictionary of events waiting to execute (event wating list).
    event_dict = {}
    lock = Lock()

    # @param timeout {Number} - the time that wait function waits for a key to send.
    def __init__(self, timeout=10.0):
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
