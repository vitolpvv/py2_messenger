import inspect


class Log:

    def __init__(self, logger=None):
        self._logger = logger

    def __call__(self, func):
        def new_func(*args, **kwargs):
            if self._logger:
                self._logger.info('{}.{} вызвана из {}'.format(func.__module__, func.__name__, inspect.stack()[1][3]))
            else:
                print('{}.{} вызвана из {}'.format(func.__module__, func.__name__, inspect.stack()[1][3]))
            return func(*args, **kwargs)
        return new_func
