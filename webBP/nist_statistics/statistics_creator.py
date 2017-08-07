from os.path import join, dirname, abspath


class StatisticsCreator:
    def __init__(self, pool, logger, config_storage):
        self.pool = pool
        self.logger = logger
        self.config_storage = config_storage

        this_dir = dirname(abspath(__file__))
        with open(join(this_dir, 'templates', 'template1.txt'), 'r') as f:
            self.template1 = f.read()
        with open(join(this_dir, 'templates', 'template2.txt'), 'r') as f:
            self.template2 = f.read()
        with open(join(this_dir, 'templates', 'template3.txt'), 'r') as f:
            self.template3 = f.read()

    def compute_statistics(self, group_id):
        return

    def prepare_file(self, group_id):
        file_name = join(self.config_storage.path_to_users_dir, self.config_storage.groups, str(group_id))
        with open(file_name, 'w') as f:
            f.write(self.template1)
            f.write(self.template2)
            f.write(self.template3)


