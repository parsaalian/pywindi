from threading import Event, Lock

# TODO: Add conditional event in manager

class EventManager:
    """The event manager is an object to control the events.
    It provides two basic functions, send and wait and has
    a dictionary of events, which the keys are event keys and
    the values are event objects.

    :param timout: the time to wait before stop waiting.
    """

    def __init__(self, timeout=None):
        self.timeout = timeout
        #: Dictionary of events waiting to execute (event wating list).
        self.event_dict = {}
        self.condition_dict = {}
        self.lock = Lock()


    def send(self, key, value=None):
        """This function should be called when an event has
        happened and we know that some other function may be
        or will be waiting for that event. So it fires the event
        in event dictionary.

        :param key: key of the event in event dictionary.
        """
        already_exists = key in self.event_dict

        #: Locks the event dictionary so no other changes can happen
        #: to it, during this change.
        self.lock.acquire()

        #: Make an event in dictionary if it is not availabe.
        #: It happens when no one is waiting for the event right
        #: now, but may be waiting for that in the future.
        if not already_exists:
            e = Event()
            self.event_dict[key] = e
        #: Runs if someone is already waiting for the event to happen.
        else:
            e = self.event_dict[key]

        #: Unlock dictionary.
        self.lock.release()
        if value is None:
            e.set()
        else:
            if already_exists and self.condition_dict[key](value):
                e.set()
            else:
                console.log('still waiting')


    def wait(self, key, condition=None, timeout=None):
        """When you want to wait for a value to be set, you
        can call this function and it waits the program until
        the send function for the same key is called.

        :param key: key of the event in dictionary.
        """
        timeout = self.timeout if timeout == None else timeout
        #: Locks the event dictionary so no other changes can happen
        #: to it, during this change.
        self.lock.acquire()

        #: Makes the event if it is not already availabe in the dictionary.
        if not key in self.event_dict:
            e = Event()
            self.event_dict[key] = e
            if condition is not None:
                self.condition_dict[key] = condition
        #: Runs if event is already available in dictionary. In case the
        #: event has been set before the wait or it has been called with
        #: wait function before this call.
        else:
            e = self.event_dict[key]

        #: Unlock dictionary.
        self.lock.release()
        e.wait(timeout)


class Queue:
    """This is a data structure for waiting queue. Elements in the queue
    has an id, which is the number of elements pushed before the element.
    Elements can not be popped before being pushed.

    :param limit: the maximum number of elements in the queue.
    """

    def __init__(self, limit=50):
        self.overflow_limit = limit
        self.event_manager = EventManager()
        self.push_counter = 0
        self.pop_counter = 0
        self.queue = []

    def push(self, item):
        """This function adds the element to the queue. And set the event
        with the push counter key.

        :param item: element to be pushed to the queue.
        """

        #: Overflow condition. If overflow is occured, the new item will not
        #: be added to the queue.
        if len(self.queue) == self.overflow_limit:
            print('Queue is full.')
            return
        self.queue.append(item)
        self.event_manager.send(self.push_counter)
        self.push_counter += 1

    def pop(self, timeout=None):
        """This function get the element at the start of the queue, if it
        is available. Being available means that element if pushed before
        it is popped. If the element is not pushed, it waits until it is.
        """

        #: Waiting for the element to be pushed.
        self.event_manager.wait(self.pop_counter, None, timeout)
        if len(self.queue) == 0:
            return None
        self.pop_counter += 1
        item = self.queue[0]
        #: deleting the element from the queue.
        self.queue = self.queue[1:]
        return item
