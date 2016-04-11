from controllers.common_controller import not_found, error_occurred
from controllers.login_controller import login


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

    def get_error_controller(self):
        return error_occurred