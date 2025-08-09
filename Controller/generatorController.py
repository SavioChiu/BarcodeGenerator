import os.path

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from View.generatorView_v3 import Ui_Generator
from Controller.resultPopupController import PopupWindow
from Service import barcodeGenSvc_OOP
from Service import LoggingSvc


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Generator()
        self.ui.setupUi(self)
        self.logger = LoggingSvc.Logger(filename='iconsBarcodeGenerator')
        self.modeCheck()

        # Connect the button to a function
        self.ui.genButton.clicked.connect(self.doGenBarcode)
        self.ui.clearButton.clicked.connect(self.clearAll)
        self.ui.savePathButton.clicked.connect(self.setImageSavePath)
        self.ui.batchSaveButton.clicked.connect(self.setBatchSavePath)
        self.ui.csvUploadButton.clicked.connect(self.setCsvFilePath)
        self.ui.saveAsCheckBox.clicked.connect(self.saveAsPdfCheck)
        self.ui.saveAsPdfButton.clicked.connect(self.setPdfFilePath)
        self.ui.isBatchMode.clicked.connect(self.modeCheck)
        self.ui.barcodeHead.textChanged.connect(
            lambda: self.ui.barcodeBody.setFocus() if len(self.ui.barcodeHead.text()) == 3 else True
        )
        self.ui.barcodeBody.textChanged.connect(
            lambda: self.ui.barcodeTail.setFocus() if len(self.ui.barcodeBody.text()) == 3 else True
        )
        self.ui.barcodeTail.textChanged.connect(
            lambda: self.ui.savePathButton.setFocus() if len(self.ui.barcodeTail.text()) == 6 else True
        )

    @staticmethod
    def showPopUp(msg:str):
        popup = PopupWindow()
        popup.setPopUpMessage(msg)
        popup.exec_()

    def saveAsPdfCheck(self):
        if self.ui.saveAsCheckBox.isChecked():
            self.ui.saveAsPdfDisplay.setDisabled(False)
            self.ui.saveAsPdfButton.setDisabled(False)
        else:
            self.ui.saveAsPdfDisplay.setDisabled(True)
            self.ui.saveAsPdfButton.setDisabled(True)

    def modeCheck(self):

        if self.ui.isBatchMode.isChecked():
            # disable signal mode component
            self.ui.barcodeHead.setDisabled(True)
            self.ui.barcodeBody.setDisabled(True)
            self.ui.barcodeTail.setDisabled(True)
            self.ui.savePathButton.setDisabled(True)
            self.ui.extensionComboBox.setDisabled(True)
            self.ui.savePathDisplay.setDisabled(True)
            # enable batch mode component
            self.ui.csvPathDisplay.setDisabled(False)
            self.ui.csvUploadButton.setDisabled(False)
            self.ui.batchSaveButton.setDisabled(False)
            self.ui.batchSaveDisplay.setDisabled(False)
            self.ui.saveAsCheckBox.setDisabled(False)
            self.ui.saveAsPdfDisplay.setDisabled(True)
            self.ui.saveAsPdfButton.setDisabled(True)

        else:
            # disable batch mode component
            self.ui.csvPathDisplay.setDisabled(True)
            self.ui.csvUploadButton.setDisabled(True)
            self.ui.batchSaveButton.setDisabled(True)
            self.ui.batchSaveDisplay.setDisabled(True)
            self.ui.saveAsCheckBox.setDisabled(True)
            # enable signal mode component
            self.ui.barcodeHead.setDisabled(False)
            self.ui.barcodeBody.setDisabled(False)
            self.ui.barcodeTail.setDisabled(False)
            self.ui.savePathButton.setDisabled(False)
            self.ui.extensionComboBox.setDisabled(False)
            self.ui.savePathDisplay.setDisabled(False)

    def doGenBarcode(self):
        self.logger.infoLog("doGenBarcode Start")

        self.logger.infoLog(f"isBatchMode:[{self.ui.isBatchMode.isChecked()}]")
        if not self.ui.isBatchMode.isChecked():
            # signal mode
            try:
                self.logger.infoLog(
                    f"outputFile:[{self.ui.savePathDisplay.text()}], "
                    f"barcodeData:[{self.ui.barcodeHead.text()+self.ui.barcodeBody.text()+self.ui.barcodeTail.text()}],"
                    f" savePath:[{self.ui.savePathDisplay.text()}]"
                )
                generator = barcodeGenSvc_OOP.BarcodeGenerate(outputFile=self.ui.savePathDisplay.text())
                generator.barcodeGenerate(
                    barcodeData=self.ui.barcodeHead.text() + self.ui.barcodeBody.text() + self.ui.barcodeTail.text(),
                    savePath=self.ui.savePathDisplay.text()
                )
                self.logger.infoLog(f"is Barcode Generated :[{os.path.isfile(self.ui.savePathDisplay.text())}]")
                if os.path.isfile(self.ui.savePathDisplay.text()):
                    self.showPopUp(msg=f"Generate barcode success\nfile saved in \n[{self.ui.savePathDisplay.text()}]")
                else:
                    self.showPopUp(msg=f"Generate barcode failed")

            except Exception as e:
                self.showPopUp(msg=f"Generate barcode failed\n[{e}]")
                self.logger.criticalLog()

        if self.ui.isBatchMode.isChecked():
            # batch mode
            csvFile = os.path.basename(self.ui.csvPathDisplay.text())
            folder = self.ui.csvPathDisplay.text().replace(csvFile, '')

            self.logger.infoLog(f"folder:[{folder}], inputFile:[{csvFile}], "
                                f"savePath:[{self.ui.batchSaveDisplay.text()}]")
            try:
                generator = barcodeGenSvc_OOP.BarcodeGenerate(
                    folder=folder, inputFile=csvFile, outputFile=""
                )
                barcodeData = generator.getBarcodeData()
                imageList = generator.barcodeGenerate(
                    barcodeData=barcodeData, savePath=self.ui.batchSaveDisplay.text()
                )
                self.logger.infoLog(f"Total Barcode Data: [{len(barcodeData)}], "
                                    f"Total Barcode Image: [{len(imageList)}]")

                generatedImageCnt = 0
                for image in imageList:
                    if os.path.isfile(image):
                        generatedImageCnt += 1

                if generatedImageCnt == len(imageList):
                    self.showPopUp(
                        msg=f"ALL Barcode Generated\nfiles saved in [{self.ui.batchSaveDisplay.text()}]"
                    )
                else:
                    self.showPopUp(
                        msg=f"Barcode Partially Generated\n"
                            f"success: [{len(os.listdir(self.ui.batchSaveDisplay.text()))}]\n"
                            f"failed :[{len(imageList)-len(os.listdir(self.ui.batchSaveDisplay.text()))}]\n"
                            f"file saved in [{self.ui.batchSaveDisplay.text()}]"
                    )

                self.logger.infoLog(f"Is Save As PDF file: [{self.ui.saveAsCheckBox.isChecked()}]")

                if self.ui.saveAsCheckBox.isChecked():

                    pdfFile = os.path.basename(self.ui.saveAsPdfDisplay.text())
                    pdfRoot = self.ui.saveAsPdfDisplay.text().replace(pdfFile,'')

                    self.logger.infoLog(f"pdfRoot:[{pdfRoot}], pdfFile: [{pdfFile}] "
                                        f"imageList length:[{len(imageList)}]")

                    generator = barcodeGenSvc_OOP.BarcodeGenerate(folder="", inputFile="", outputFile=pdfFile)
                    generator.saveAsPdf(savePath=pdfRoot, imageList=imageList, barcodes_per_row=4)

                    self.logger.infoLog(f"is PDF Created:[{os.path.isfile(self.ui.saveAsPdfDisplay.text())}]")

                    if os.path.isfile(self.ui.saveAsPdfDisplay.text()):
                        self.showPopUp(
                            msg=f"Generate PDF success\nfile saved in [{self.ui.saveAsPdfDisplay.text()}]"
                        )
                    else:
                        self.showPopUp(msg=f"Generate PDF failed")

            except Exception as e:
                self.showPopUp(msg=f"Generate barcode failed\n{e}")
                self.logger.criticalLog()

    def clearAll(self):
        self.logger.infoLog("clearAll Start")
        self.ui.barcodeHead.clear()
        self.ui.barcodeBody.clear()
        self.ui.barcodeTail.clear()
        self.ui.savePathDisplay.clear()

        self.ui.csvPathDisplay.clear()
        self.ui.batchSaveDisplay.clear()

        self.ui.saveAsCheckBox.setChecked(False)
        self.ui.saveAsPdfDisplay.clear()
        self.saveAsPdfCheck()

    def setImageSavePath(self):
        selectedType = self.ui.extensionComboBox.currentText()
        filePath, fileType = QFileDialog.getSaveFileUrl(self, "Save Barcode Image", "",
                                                        f"Image File (*.{selectedType});; All Files(*)", "")
        self.logger.infoLog(f"filePath:{filePath.toLocalFile()}, fileType:{fileType}")

        self.ui.savePathDisplay.setReadOnly(False)
        self.ui.savePathDisplay.clear()
        self.ui.savePathDisplay.setText(filePath.toLocalFile())
        self.ui.savePathDisplay.setReadOnly(True)

    def setBatchSavePath(self):
        folderPath = QFileDialog.getExistingDirectoryUrl(self, "Save Barcode Image")
        # print(f"folderPath:{folderPath.toLocalFile()}")
        self.logger.infoLog(f"folderPath:{folderPath.toLocalFile()}")

        self.ui.batchSaveDisplay.setReadOnly(False)
        self.ui.batchSaveDisplay.clear()
        self.ui.batchSaveDisplay.setText(folderPath.toLocalFile())
        self.ui.batchSaveDisplay.setReadOnly(True)

    def setCsvFilePath(self):
        filePath, fileType = QFileDialog.getOpenFileName(self, "Select Barcode Data", "",
                                                         f"CSV File (*.csv)", "")
        self.logger.infoLog(f"filePath:{filePath}, fileType:{fileType}")

        self.ui.csvPathDisplay.setReadOnly(False)
        self.ui.csvPathDisplay.clear()
        self.ui.csvPathDisplay.setText(filePath)
        self.ui.csvPathDisplay.setReadOnly(True)

    def setPdfFilePath(self):
        filePath, fileType = QFileDialog.getSaveFileUrl(self, "Save Barcode Image into PDF", "",
                                                        f"PDF File (*.pdf)", "")
        self.logger.infoLog(f"filePath:{filePath}, fileType:{fileType}")

        self.ui.saveAsPdfDisplay.setReadOnly(False)
        self.ui.saveAsPdfDisplay.clear()
        self.ui.saveAsPdfDisplay.setText(filePath.toLocalFile())
        self.ui.saveAsPdfDisplay.setReadOnly(True)
