class ConfigStorage:

    def __init__(self, parser):
        """
        Initializes class ConfigStorage. This class is used for getting options for setting application. Once
        initialized, their attributes should never be modified.
        :param parser: Parser from which values associated to keys can be get.
        """
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
        self.sched_id_of_pid = parser.get_key('SCHEDULER_ID_OF_PID')
        self.server_key = parser.get_key('SERVER_KEY')
        self.server_cert = parser.get_key('SERVER_CERT')
        self.ca_certs = parser.get_key('CA_CERTS')
        self.groups = parser.get_key('GROUPS')
        self.path_to_pdf_texts = parser.get_key('PATH_TO_PDF_TEXTS')
        self.path_to_tex_templates = parser.get_key('PATH_TO_TEX_TEMPLATES')
