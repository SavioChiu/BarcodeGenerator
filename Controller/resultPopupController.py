from PyQt5.QtWidgets import QDialog
from View.resultPopupView_v1 import Ui_popup


class PopupWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_popup()
        self.ui.setupUi(self)
        self.ui.exitButton.clicked.connect(self.close)

    def setPopUpMessage(self,msg:str):
        self.ui.messageArea.setText(msg)
