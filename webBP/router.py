from controllers.common_controller import not_found, error_occurred
from controllers.login_controller import login


class Router:
    def __init__(self):
        """
        Initializes dictionary _controllers.
        """
        self._controllers = {}

    def register_controller(self, path, controller):
        """
        Registers function controller under key path.
        :param path: URL path that has mapped controller on it.
        :param controller: Controller for param path.
        """
        self._controllers[path] = controller

    def default_controller(self):
        """
        Returns default controller.
        :return: Function not_found.
        """
        return not_found

    def get_controller(self, path):
        """
        Searches for path and if search succeeds, returns associated controller - function pointer.
        :param path: Path for which controller is searched.
        :return: If key path exists then associated controller to it. Default controller otherwise.
        """
        function = self._controllers.get(path)
        if function:
            return function
        return self.default_controller()

    def get_login_controller(self):
        """
        Returns login controller.
        :return: Login controller function.
        """
        return login

    def get_error_controller(self):
        """
        Returns error controller.
        :return: Error controller function.
        """
        return error_occurred
