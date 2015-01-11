class OptimisticDict(dict):

    def __init__(self, factory_func):
        self.factory_func = factory_func
        super(OptimisticDict, self).__init__()

    def __missing__(self, key):
        self[key] = self.factory_func(key)
        return self.factory_func(key)
