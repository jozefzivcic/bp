class Group:

    def __init__(self):
        self.id = 0
        self.user_id = 0
        self.time_of_add = 0
        self.test_id_arr = []

    def get_num_of_tests(self):
        return len(self.test_id_arr)