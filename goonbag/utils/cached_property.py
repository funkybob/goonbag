

class cached_property:
    def __init__(self, func, name=None):
        self.func = func
        self.name = name or func.__name__

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        value = instance.__dict__[self.name] = self.func(instance)
        return value
