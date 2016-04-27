class ConfigStorage:

    def __init__(self, parser):
        self.database = parser.get_key('DATABASE')
        self.user_name = parser.get_key('USERNAME')
        self.user_password = parser.get_key('USER_PASSWORD')
        self.schema = parser.get_key('SCHEMA')
        self.nist = parser.get_key('NIST')
        self.tests_results = parser.get_key('TESTS_RESULTS')
        self.ip_address = parser.get_key('IP_ADDRESS')
        self.port = int(parser.get_key('PORT'))
        self.pooled_connections = int(parser.get_key('POOLED_CONNECTIONS_FOR_WEB'))
        self.path_to_users_dir = parser.get_key('PATH_TO_USERS_DIR_FROM_WEB')
        self.files = parser.get_key('FILES')
