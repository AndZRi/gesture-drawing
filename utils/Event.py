from collections.abc import Callable

class Event:
    def __init__(self):
        self.listeners = []

    def fire(self):
        for func, args, kwargs in self.listeners:
            func(*args, **kwargs)

    def __call__(self):
        self.fire()

    def add_listener(self, func: Callable[[...], ...], *args, **kwargs):
        self.listeners.append((func, args, kwargs))
