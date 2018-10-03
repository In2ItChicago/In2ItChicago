from threading import Condition, Lock, Thread

class UpdateLock:
    def __init__(self):
        self.lock = Lock()
        self.updating_cond = Condition()
        self.is_updating = False
        
    def wait_for_clearance(self):
        if self.is_updating:
            with self.updating_cond:
                self.updating_cond.wait_for(lambda: self.is_updating == False)

    def start_update(self):
        self.lock.acquire()
        self.is_updating = True
    
    def finish_update(self):
        self.lock.release()
        self.is_updating = False
        with self.updating_cond:
            self.updating_cond.notify_all()
    
    def __enter__(self):
        self.start_update()
    
    def __exit__(self, type, value, traceback):
        self.finish_update()

class QueryLock:
    def __init__(self):
        self.lock = Lock()
        self.counter_lock = Lock()
        self.query_cond = Condition()
        self.counter = 0
        
    def wait_for_clearance(self):
        if self.counter > 0:
            with self.query_cond:
                self.query_cond.wait_for(lambda: self.counter == 0)

    def change_counter(self, value):
        self.counter_lock.acquire()
        self.counter += value
        self.counter_lock.release()

    def start_query(self):
        self.change_counter(+1)
    
    def finish_query(self):
        self.change_counter(-1)
        if self.counter == 0:
            with self.query_cond:
                self.query_cond.notify_all()

    def __enter__(self):
        self.start_query()
    
    def __exit__(self, type, value, traceback):
        self.finish_query()