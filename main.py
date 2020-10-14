from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import time

from src import MainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow.MainWindow()
    sys.exit(app.exec_())