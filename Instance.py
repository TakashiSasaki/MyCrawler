

class Singleton(type): 
    def __init__(self, *args): 
        type.__init__(self, *args) 
        self._instances = {}

    def __call__(self, *args): 
        if not args in self._instances: 
            self._instances[args] = type.__call__(self, *args) 
            return self._instances[args]

