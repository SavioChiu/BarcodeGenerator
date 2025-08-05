import os
import sys

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

from Service import LoggingSvc
from Controller.generatorController import MainWindow


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


if __name__ == "__main__":
    logger = LoggingSvc.Logger(filename='iconsBarcodeGenerator')
    logger.infoLog("Icons Barcode Generator GUI start")
    app = QtWidgets.QApplication([])
    app.setWindowIcon(QIcon(resource_path("Resource/generator-icon.png")))
    window = MainWindow()
    window.show()
    app.exec_()

    logger.infoLog("Icons Barcode Generator GUI end")
