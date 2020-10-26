from PyQt5 import QtCore, QtGui, QtWidgets
import sys

from src.ui import Ui_About

class MainWindow(QtWidgets.QDialog, Ui_About.Ui_Dialog):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
