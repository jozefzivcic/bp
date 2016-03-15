import managers.connectionpool

class UserManager:
    def __init__(self, con_pool):
        self.nieco = ''
        self.pool = con_pool
    def saveUser(self, user):
        connection = self.pool.get_connection_from_pool()
        cur = connection.cursor()
        cur.execute()