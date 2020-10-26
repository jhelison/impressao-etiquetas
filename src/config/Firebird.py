import fdb

class Firebird():
    def __init__(self, databaseLocation, login, password):
        con = fdb.connect(databaseLocation,
                                login,
                                password)

        self.cur = con.cursor()