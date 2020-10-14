from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import fdb
import time

from src.ui import Ui_Main

from src.config.Firebird import Firebird
from src.api.FBprodutos import FBprodutos

from src.utils.QTableWidgetHandler import QTableWidgetHandler

class MainWindow(QtWidgets.QMainWindow, Ui_Main.Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        
        #Database setup
        cur = Firebird().cur
        fBprodutos = FBprodutos(cur)
        
        QTableWidgetHandler(self.vlInputTW, self.tableWidget_2, dataBaseAPI = fBprodutos, addPaging=True, addFilter=True)
        
        
        self.updateStatusBar()

        self.show()
        
    def updateStatusBar(self):
        self.statusbar = QtWidgets.QStatusBar()
        self.statusBar().showMessage('Banco de dados não configurado')