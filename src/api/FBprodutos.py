import fdb
import time

class FBprodutos():
    def __init__(self, cur):
        self.cur = cur
        
        self.COLUMNS = [column[0].strip() for column in self.cur.execute("""SELECT rdb$field_name 
                                                                        FROM rdb$relation_fields 
                                                                        WHERE rdb$relation_name=\'PRODUTO\' 
                                                                        ORDER BY rdb$field_position""").fetchall()]
                        
        self.dataLen = self.getDataLen()
        self.totalLen = self.dataLen

    def get(self, page = 1, limit = 0, filter = [None, None]):
        data = {}
        data['columns'] = self.COLUMNS
        
        if limit:
            pagingSQL = f"FIRST {limit} SKIP {(page - 1) * limit}"
        else:
            pagingSQL = ""
        
        if filter[1]:
            filterSQL = f"WHERE {filter[0]} LIKE \'%{filter[1]}%\'"
        else:
            filterSQL = ""
            
        fullSql = f"SELECT {pagingSQL} * FROM PRODUTO {filterSQL}"
        
        data['data'] = self.cur.execute(fullSql).fetchall()
        
        if filter[1]:
            fullSQL = f"SELECT COUNT(CODPROD) FROM PRODUTO {filterSQL}"
            self.dataLen = self.cur.execute(fullSQL).fetchall()[0][0]
        else:
            self.dataLen = self.totalLen

        return data
    
    def getDataLen(self):
        fullSql = "SELECT COUNT(CODPROD) FROM PRODUTO"
        return self.cur.execute(fullSql).fetchall()[0][0]
    