import sys
import math

import barcode
from barcode.writer import *

from PIL import ImageFont

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm


class BarcodeGenerate:

    def __init__(self, folder=os.path.curdir, inputFile="barcodeData.csv", outputFile="barcode.pdf"):
        self.rootPath = os.path.abspath(folder)
        self.csvPath = self.findFile(inputFile)
        self.outName = outputFile

    @staticmethod
    def __resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    def findFile(self, filename:str) -> os.path:
        csvDir = os.path.join(os.path.abspath(self.rootPath), filename)
        if os.path.isfile(csvDir): return csvDir
        # search file
        for root, folder, fileList in os.walk(os.path.abspath(self.rootPath)):
            if filename in fileList:
                return os.path.join(root,filename)

    def getBarcodeData(self) -> [str]:
        return [line.replace(',','').replace('\n','') for line in open(self.csvPath)]

    def barcodeGenerate(self, barcodeData:[str], savePath:os.path):
        if len(barcodeData) <= 0:
            # print("No barcode Data")
            return
        if type(barcodeData) == str:
            return self.__singleGen(barcodeData, savePath)
        if type(barcodeData) == list:
            return self.__batchGen(barcodeData, savePath)

    def __singleGen(self, barcodeData:str, savePath:os.path):
        filename = self.outName
        extension = 'png'
        if "." in filename:
            extension = filename.split('.')[-1]
            filename = filename.split('.')[0]
        # print(f"filename:[{filename}], extension:[{extension}]")
        self.__barcodeGen(barcodeData=barcodeData,savePath=savePath,filename=filename, extension=extension)
        return os.path.join(savePath,f"{filename}.{extension}")

    def __batchGen(self, barcodeData:list, savePath:os.path):
        imageList = []
        for data in barcodeData:
            self.__barcodeGen(barcodeData=data, savePath=savePath, filename=data, extension='png')
            imageList.append(os.path.join(savePath,f"{data}.png"))
        return imageList

    def __barcodeGen(self,barcodeData:str, savePath:os.path, filename:str, extension:str):
        image = os.path.join(savePath, filename)

        # for prevent ImageFont OSError
        writer = ImageWriter()
        writer.font_path = self.__resource_path("Resource/DejaVuSansMono.ttf")
        writer.format = extension

        content = barcode.get('code128', barcodeData, writer=writer)
        content.save(image)

    @staticmethod
    def __paging(itemList:list, maxColumn:int, maxRow:int):
        pagingMap = []
        maxPerPage = maxColumn*maxRow

        while len(itemList) > maxPerPage:
            pagingMap.append(itemList[0:maxPerPage])
            for item in itemList[0:maxPerPage]:
                itemList.remove(item)

        if len(itemList) > 0:
            pagingMap.append(itemList)
        # print(f"page:[{len(pagingMap)}]")
        return pagingMap

    def saveAsPdf(self, savePath:os.path, imageList: [os.path], barcodes_per_row:int):
        pdfFile = os.path.join(savePath,self.outName)
        c = canvas.Canvas(pdfFile, pagesize=A4)
        width, height = A4

        # Layout settings
        x_offset = 10 * mm
        y_offset = height - 30 * mm
        barcode_width = 40 * mm
        barcode_height = 20 * mm
        spacing_x = 10 * mm
        spacing_y = 5 * mm

        maxRowPerPage = math.floor(y_offset/(barcode_height + spacing_y))
        # print(f"barcodes_per_row:[{barcodes_per_row}], maxRowPerPage:[{maxRowPerPage}]")
        pdfPagingMap = self.__paging(itemList=imageList, maxColumn=barcodes_per_row, maxRow=maxRowPerPage)

        # print(pdfPagingMap)
        for page in pdfPagingMap:
            for index, image_path in enumerate(page):
                # Calculate position
                row = index // barcodes_per_row
                col = index % barcodes_per_row
                x = x_offset + (barcode_width + spacing_x) * col
                y = y_offset - (barcode_height + spacing_y) * row

                c.drawImage(image_path, x, y, width=barcode_width, height=barcode_height)
            if pdfPagingMap.index(page)+1 < len(pdfPagingMap):
                if len(pdfPagingMap[pdfPagingMap.index(page)+1]) > 0:
                    c.showPage()

        # Finalize PDF
        c.save()
