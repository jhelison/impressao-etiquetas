from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import fdb
import os

from src.ui import Ui_DatabaseConfig

from src.config.ConfigDB import ConfigDB


class MainWindow(QtWidgets.QDialog, Ui_DatabaseConfig.Ui_Dialog):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        
        self.arrangeUIFromDB()
        
        self.pbEncontrar.clicked.connect(self.pbFindDatabase)
        self.pdFindOutput.clicked.connect(self.pbFindOutputFolder)
        self.pbApply.clicked.connect(self.checkIfApplyValid)
        self.pbCancel.clicked.connect(self.pbCancelF)
        
    def arrangeUIFromDB(self):
        self.db = ConfigDB()
        
        self.leDBFile.setText(self.db.get("leDBFile"))
        self.leLogin.setText(self.db.get("leLogin"))
        self.lePassword.setText(self.db.get("lePassword"))
        self.leOutuput.setText(self.db.get("leOutuput"))
        
    def pbFindDatabase(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self,
                                                          'Arquivo do banco de dados',
                                                          self.db.get('leDBFile'),
                                                          "Arquivo Firebird (*.FDB *.fdb)")[0]
                
        self.leDBFile.setText(path)
        
    def pbFindOutputFolder(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                          'Pasta de saída',
                                                          self.db.get('leOutuput'))
                
        self.leOutuput.setText(path)
        
    def checkIfApplyValid(self):
        if not os.path.exists(self.leDBFile.text()):
            self.show_error("Caminho do arquivo do banco de dados invalido")
            return
        if not os.path.exists(self.leOutuput.text()):
            self.show_error("Caminho de saida do arquivo invalido")
            return
        if not self.leLogin.text():
            self.show_error("O login do banco de dados não pode estar vazio")
            return
        if not self.lePassword.text():
            self.show_error("A senha do banco de dados não pode estar vazia")
            return
        try:
            con = fdb.connect(self.leDBFile.text(), self.leLogin.text(), self.lePassword.text())
            cur = con.cursor()
        except BaseException as e:
            self.show_error(str(e))
            return
        
        self.db.save('leDBFile', self.leDBFile.text())
        self.db.save('leLogin', self.leLogin.text())
        self.db.save('lePassword', self.lePassword.text())
        self.db.save('leOutuput', (self.leOutuput.text()))
        
        self.close()
        
    def pbCancelF(self):
        self.close()
    
    def show_error(self, text):
        msg = QtWidgets.QMessageBox()
        msg.setText(text)
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.exec_()
        
        