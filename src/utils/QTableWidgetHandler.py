from PyQt5 import QtCore, QtGui, QtWidgets, QtTest

import math
import sys
import time

class QTableWidgetHandler(QtWidgets.QMainWindow):
    def __init__(self, Qlayout, qTableWidget, dataBaseAPI = None, dataLimit = 50, addPaging = False, addFilter = False):
        super().__init__()
        self.Qlayout = Qlayout
        self.qTableWidget = qTableWidget
        
        if addPaging:
            self.dataLimit = dataLimit
        else:
            self.dataLimit = 0
        self.dataBaseAPI = dataBaseAPI
        
        self.selectedPage = 1
        
        self.isSetupPage = False
        
        self.filter = [None, None]
                
        if addFilter:
            self.setupFilter()
        else:
            self.fillTable(page = self.selectedPage, limit = self.dataLimit)
            
        if addPaging:
            self.setupPaging()
        
    def fillTable(self, page = 1, limit = 0, filter = [None, None]):
        """This function fill the table \n
        The data have to be a dictionary with keys columns and data"""            
        self.data = self.dataBaseAPI.get(page = page, limit = limit, filter = filter)
        
        #Columns Headers
        self.qTableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.qTableWidget.setColumnCount(len(self.data['columns']))
        self.qTableWidget.setHorizontalHeaderLabels(self.data['columns'])
        
        self.qTableWidget.setRowCount(len(self.data['data']))
        self.qTableWidget.setAlternatingRowColors(True)
        
        self.qTableWidget.setSortingEnabled(False)
        
        #self.qTableWidget.resizeColumnsToContents() SLOW!!
        
        if self.data:
            for column in range(len(self.data['columns'])):
                for row in range(len(self.data['data'])):
                    newitem = QtWidgets.QTableWidgetItem((str(self.data['data'][row][column])))
                    self.qTableWidget.setItem(row, column, newitem)
                    
        self.qTableWidget.setSortingEnabled(True)
        
    def setupFilter(self):
        self.executing = False
        name = self.qTableWidget.objectName()
        self.qTableWidget.deleteLater()
        
        self.filterLayout = QtWidgets.QHBoxLayout()
        self.filterLayout.setObjectName("filterLayout")
        self.Qlayout.addLayout(self.filterLayout)
        
        self.cbColunas = QtWidgets.QComboBox()
        self.filterLayout.addWidget(self.cbColunas)
        self.teTextFilter = QtWidgets.QLineEdit()
        self.teTextFilter.textChanged.connect(self.filterLogic)
        self.filterLayout.addWidget(self.teTextFilter)
        
        self.qTableWidget = QtWidgets.QTableWidget()
        self.qTableWidget.setObjectName(name)
        self.Qlayout.addWidget(self.qTableWidget)
        
        self.fillTable(page = self.selectedPage, limit = self.dataLimit)

        for item in self.data['columns']:
            self.cbColunas.addItem(item)

    def filterLogic(self):
        if not self.executing:
            self.executing = True
            QtTest.QTest.qWait(1000)
            selectedColumn = self.cbColunas.currentText()
            filterText = self.teTextFilter.text()
            
            self.selectedPage = 1
            self.filter = [selectedColumn, filterText]
            self.fillTable(page = self.selectedPage, limit = self.dataLimit, filter = self.filter)
                        
            if self.isSetupPage:
                self.pagingLogic()
                
            self.executing = False
             
        
    def setupPaging(self):
        """Setup the paging system \n
        It acepts a function for paging"""
        self.selectedPage = 1
        
        self.isSetupPage = True
        
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.setObjectName("buttonLayout")
        self.Qlayout.addLayout(self.buttonLayout)
        
        self.pagingLogic()

    def pagingLogic(self):
        self.dataLen = self.dataBaseAPI.dataLen
        
        self.maxPage = int((self.dataLen / self.dataLimit) + 1)
        #Clean the view
        self.cleanLayout(self.buttonLayout)
            
        #Size Policy for the buttons
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        
        if self.dataLen:
            dataInfoLabel = QtWidgets.QLabel()
            dataInfoLabel.setText(f"{((self.selectedPage - 1) * self.dataLimit) + 1} - {self.selectedPage * self.dataLimit} de {self.dataLen} registros")
            self.buttonLayout.addWidget( dataInfoLabel)
        
        leftHorizontalSpacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.buttonLayout.addItem(leftHorizontalSpacer)
        
        pageInfoLabel = QtWidgets.QLabel()
        pageInfoLabel.setText(f"{self.selectedPage} - {self.maxPage} paginas")
        self.buttonLayout.addWidget( pageInfoLabel)
                
        first_page_button = QtWidgets.QPushButton("<<")
        first_page_button.setSizePolicy(sizePolicy)
        first_page_button.setMaximumSize(QtCore.QSize(40, 16777215))
        self.buttonLayout.addWidget( first_page_button)
        first_page_button.clicked.connect(lambda _: self.updatePage(1))
        
        before_page_button = QtWidgets.QPushButton("...")
        before_page_button.setSizePolicy(sizePolicy)
        before_page_button.setMaximumSize(QtCore.QSize(40, 16777215))
        self.buttonLayout.addWidget( before_page_button)
        before_page_button.clicked.connect(lambda _: self.updatePage(self.selectedPage - 1))
        
        pageRangeIndex = (math.ceil(self.selectedPage / 5) - 1) * 5 + 1
                
        for x in range(pageRangeIndex, pageRangeIndex + 5):
            if x <= self.maxPage:
                pageButton = QtWidgets.QPushButton()
                pageButton.setText(str(x))
                pageButton.setMaximumSize(QtCore.QSize(40, 16777215))
                pageButton.setObjectName(str(x))
                pageButton.setSizePolicy(sizePolicy)
                pageButton.clicked.connect(self.updatePage)
                if self.selectedPage == x:
                    pageButton.setEnabled(False)
                self.buttonLayout.addWidget(pageButton)
                                
        after_page_button = QtWidgets.QPushButton("...")
        after_page_button.setMaximumSize(QtCore.QSize(40, 16777215))
        after_page_button.setSizePolicy(sizePolicy)
        self.buttonLayout.addWidget( after_page_button )
        after_page_button.clicked.connect(lambda _: self.updatePage(self.selectedPage + 1))
            
        last_page_button = QtWidgets.QPushButton(">>")
        last_page_button.setMaximumSize(QtCore.QSize(40, 16777215))
        last_page_button.setSizePolicy(sizePolicy)
        self.buttonLayout.addWidget( last_page_button)
        last_page_button.clicked.connect(lambda _: self.updatePage(self.maxPage))
                
        if self.selectedPage == 1:
            first_page_button.setEnabled(False)
            before_page_button.setEnabled(False)
        if self.maxPage == self.selectedPage:
            last_page_button.setEnabled(False)
            after_page_button.setEnabled(False)
    
    def updatePage(self, selectedPage = 0):
        if selectedPage == 0:
            self.selectedPage = int(self.sender().objectName())
        else:
            if selectedPage <= self.maxPage:
                self.selectedPage = selectedPage
            else:
                selectedPage = self.maxPage
                
        self.fillTable(page = self.selectedPage, limit = self.dataLimit, filter = self.filter)
        
        self.pagingLogic()
        
    def cleanLayout(self, layout):
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            
            if widget is not None:
                widget.deleteLater()
            else:
                layout.takeAt(i)

        