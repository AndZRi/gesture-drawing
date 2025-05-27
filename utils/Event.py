from collections.abc import Callable

# i surrender in making this type stricted, like why am i even doing this in python, for what
# i like it though

class Event:
    def __init__(self, return_type=None, *args_types, **kwargs_types):
        """Specify the type of a listener: Callable[*args_types, **kwargs_types] -> return_type"""

        self.return_type = return_type
        self.args_types = args_types
        self.kwargs_types = kwargs_types
        self._listeners = []

    def fire(self, *args, **kwargs):
        if len(self.args_types) != len(args):
            raise TypeError(f"Number of provided arguments does not match number of"
                            f" provided arguments types ({len(args)} != {len(self.args_types)}")
        for i, j in zip(args, self.args_types):
            if not isinstance(i, j):
                raise TypeError(f"Provided argument type ({type(i)}) does not match required ({j})")

        # just checking if kwargs types don't match or if there is an extra one
        for i in kwargs.items():
            if self.kwargs_types.get(i[0]) is None:
                raise TypeError(f"Got an unexpected keyword argument '{i[0]}'")
            if not isinstance(i[1], self.kwargs_types[i[0]]):
                raise TypeError(f"Provided argument\'s type by keyword '{i[0]}' "
                                f"({type(i)}) does not match required ({self.kwargs_types[i[0]]})")

        try:
            for func in self._listeners:
                func(*args, **kwargs)
        except TypeError:
            raise TypeError(f"Bad listener '{func.__name__}'. Good luck.")  # why is it possible you stupid bustard

    def __call__(self, *args, **kwargs):
        self.fire(*args, **kwargs)

    def add_listener(self, func: Callable[[...], ...]):
        """DOES NOT CHECK THE PROVIDED FUNCTION ARGUMENTS, BE CAREFUL"""
        self._listeners.append(func)


# a = Event(None, str, sep=str)
# a.add_listener(print)
# a.add_listener(str.__str__)
# a.fire('111', sep='dd')
