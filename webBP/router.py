from controller import not_found, login


class Router:
    def __init__(self):
        self._controllers = {}

    def register_controller(self, path, controller):
        self._controllers[path] = controller

    def default_controller(self):
        return not_found

    def get_controller(self, path):
        function = self._controllers.get(path)
        if function:
            return function
        return self.default_controller()

    def get_login_controller(self):
        return login