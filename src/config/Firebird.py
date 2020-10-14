import fdb

class Firebird():
    def __init__(self):
        con = fdb.connect(r'C:\Users\Jhelison\Documents\full python Projects\C-Plus Cadastro produtos\temp\CPLUS.FDB',
                                'sysdba',
                                'masterkey')

        self.cur = con.cursor()