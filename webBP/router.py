class Router:
    def __init__(self):
        self._contollers = {}

    def register_controller(self, path, controller):
        self._contollers[path] = controller

    def default_controller(self):
        status = '404 not found'

    def get_controller(self, path):
        function = self._contollers.get(path)
        if function:
            return function
        return self.default_controller()
