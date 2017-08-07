from os.path import join


class StatisticsCreator:
    def __init__(self, pool, logger, config_storage):
        self.pool = pool
        self.logger = logger
        self.config_storage = config_storage

        with open('./template1.txt', 'r') as f:
            self.template1 = f.read()
        with open('./template2.txt', 'r') as f:
            self.template2 = f.read()
        with open('./template3.txt', 'r') as f:
            self.template3 = f.read()

    def compute_statistics(self, group_id):
        return

    def prepare_file(self, group_id):
        file_name = join(self.config_storage.path_to_users_dir, self.config_storage.groups, str(group_id))
        with open(file_name, 'w') as f:
            f.write(self.template1)
            f.write(self.template2)
            f.write(self.template3)


