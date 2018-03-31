class Test:
    def __init__(self, test_id: int=0, file_id: int=0, user_id: int=0, time_of_add: int=0, test_table: str='',
                 loaded: int=0, ended: int=0, return_value: int=0):
        """
        Initializes object Test().
        """
        self.id = test_id
        self.file_id = file_id
        self.user_id = user_id
        self.time_of_add = time_of_add
        self.test_table = test_table
        self.loaded = loaded
        self.ended = ended
        self.return_value = return_value
