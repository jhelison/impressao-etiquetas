from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import fdb
import time
import os

from src.ui import Ui_Main

from src.config.Firebird import Firebird
from src.api.FBprodutos import FBprodutos

from src.utils.Paper import Paper

from src.utils.QTableWidgetHandler import QTableWidgetHandler

from src import DatabaseConfig

class MainWindow(QtWidgets.QMainWindow, Ui_Main.Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        
        #Database setup
        cur = Firebird().cur
        fBprodutos = FBprodutos(cur)
        
        QTableWidgetHandler(self.vlInputTW, self.tableWidget_2, dataBaseAPI = fBprodutos, addPaging=True, addFilter=True)
        
        self.setupQtableWidget()
                
        self.updateStatusBar()
        
        self.pbAdd.clicked.connect(self.addOutputRow)
        self.pbRemove.clicked.connect(self.removeOutputRow)
        self.pbGenerate.clicked.connect(self.generate)
        
        self.actionBanco_de_dados.triggered.connect(self.openDatabaseConfig)

        self.showMaximized()
        
    def updateStatusBar(self):
        self.statusbar = QtWidgets.QStatusBar()
        self.statusBar().showMessage('Banco de dados não configurado')
    
    def setupQtableWidget(self):
        self.twOutputItens.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.twOutputItens.setColumnCount(4)
        self.twOutputItens.setHorizontalHeaderLabels(["Codigo", "NomeProduto", "Preço", "Quantidade"])
        
    def addOutputRow(self):
        table = self.findChild(QtWidgets.QTableWidget, "tableWidget_2")
        items = table.selectedItems()
        
        outputNumRows = self.twOutputItens.rowCount()
        self.twOutputItens.setRowCount(outputNumRows + 1)
        
        for index, item in enumerate(items):
            newItem = QtWidgets.QTableWidgetItem(item.text())
            self.twOutputItens.setItem(outputNumRows, index,newItem)
        spinBoxWidget = QtWidgets.QSpinBox()
        spinBoxWidget.setMinimum(1)
        self.twOutputItens.setCellWidget(outputNumRows, 3, spinBoxWidget)
        self.twOutputItens.resizeColumnsToContents()

    def removeOutputRow(self):
        table = self.findChild(QtWidgets.QTableWidget, "twOutputItens")
        items = table.selectedIndexes()
        
        if items:
            table.removeRow(items[0].row())
            
    def generate(self):
        rows = self.twOutputItens.rowCount()

        data = []
        
        for row in range(rows):
            data.append([self.twOutputItens.item(row, 0).text(),
                         self.twOutputItens.item(row, 1).text(),
                         self.twOutputItens.item(row, 2).text(),
                         self.twOutputItens.cellWidget(row, 3).value()])
            
        paper = Paper()
        paper.buildPaper(data, self.sbHorizontalPos.value(), self.sbVerticalPos.value())
        
    def openDatabaseConfig(self):
        configDialog = DatabaseConfig.MainWindow()
        configDialog.exec()
            
                