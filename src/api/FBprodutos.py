import fdb
import time

class FBprodutos():
    def __init__(self, cur):
        self.cur = cur
        
        self.COLUMNS = ["CODIGO", "NOMEPROD", "PRECO"]
                        
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
            filterSQL = f"AND {filter[0]} LIKE \'%{filter[1]}%\'"
        else:
            filterSQL = ""
            
        fullSql = f"SELECT {pagingSQL} CODIGO, NOMEPROD, PRECO FROM PRODUTO LEFT JOIN PRODUTOPRECO ON PRODUTO.CODPROD = PRODUTOPRECO.CODPROD WHERE CODPRECO = 1 {filterSQL}"
        
        print("SQL GET 1 ", fullSql)
        
        data['data'] = self.cur.execute(fullSql).fetchall()
        
        if filter[1]:
            fullSQL = f"SELECT COUNT(CODIGO) FROM PRODUTO LEFT JOIN PRODUTOPRECO ON PRODUTO.CODPROD = PRODUTOPRECO.CODPROD WHERE CODPRECO = 1 {filterSQL}"
            print("SQL GET 2 ", fullSql)
            self.dataLen = self.cur.execute(fullSQL).fetchall()[0][0]
        else:
            self.dataLen = self.totalLen

        return data
    
    def getDataLen(self):
        fullSql = "SELECT COUNT(CODIGO) FROM PRODUTO LEFT JOIN PRODUTOPRECO ON PRODUTO.CODPROD = PRODUTOPRECO.CODPROD WHERE CODPRECO = 1"
        print("SQL GETDATALEN ", fullSql)
        return self.cur.execute(fullSql).fetchall()[0][0]
    