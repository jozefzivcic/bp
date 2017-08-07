from os.path import join, dirname, abspath, exists

from os import makedirs


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
        self.template2 = self.template2[:-1]
        with open(join(this_dir, 'templates', 'template3.txt'), 'r') as f:
            self.template3 = f.read()

    def compute_statistics(self, group_id, user_id):
        return

    def prepare_file(self, group_id, user_id, file):
        dir_name = join(self.config_storage.path_to_users_dir, str(user_id), self.config_storage.groups, str(group_id))
        if not exists(dir_name):
            makedirs(dir_name)
        file_name = 'grp_' + str(group_id) + '_f_' + str(file.id)
        file_loc = join(dir_name, file_name)
        to_write = self.template1 + self.template2 + ' <' + file.name + '>\n' + self.template3
        with open(file_loc, 'w') as f:
            f.write(to_write)


