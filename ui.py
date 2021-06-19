#-*-coding:utf-8-*-

import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5 import uic
from zoomInterface import ZoomInterface

form_class = uic.loadUiType("zoomcc.ui")[0]

class WindowClass(QDialog, form_class) :
    lylicdir = "가사"
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.zoom = ZoomInterface.instance()
        self.lylicNotShow.setChecked(True)

        self.urlSet.clicked.connect(lambda: self.zoom.setURL(self.url.text()))
        self.url.returnPressed.connect(lambda: self.zoom.setURL(self.url.text()))
        self.open.clicked.connect(self.loadLylics)
        self.fileName.returnPressed.connect(self.loadLylics)
        self.lylic.currentItemChanged.connect(self.sendLylic)
        self.past.clicked.connect(self.setPast)
        self.next.clicked.connect(self.setNext)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Right or e.key() == Qt.Key_Down:
            self.setNext()
        elif e.key() == Qt.Key_Left or e.key() == Qt.Key_Up:
            self.setPast()
        else :
            super().keyPressEvent(e)

    def loadLylics(self):
        fileName = os.path.join(self.lylicdir, self.fileName.text())
        if os.path.isfile(fileName) == False:
            QMessageBox.information(self, "QMessageBox", fileName + ": 파일이 존재하지 않습니다.")
            return
        f = open(fileName, 'r')
        lylics = f.readlines()
        f.close()
        self.lylic.clear()
        for lylic in lylics:
            self.lylic.addItem(lylic)
        if self.lylic.count() > 0:
            self.lylic.item(0).setSelected(True)
            self.lylic.setCurrentRow(0)

    def setPast(self):
        if self.lylic.count() <= 0 or self.lylic.currentRow() <= 0:
            return
        self.lylic.item(self.lylic.currentRow()).setSelected(False)
        self.lylic.item(self.lylic.currentRow() - 1).setSelected(True)
        self.lylic.setCurrentRow(self.lylic.currentRow() - 1)

    def setNext(self):
        if self.lylic.count() <= 0 or self.lylic.currentRow() >= (self.lylic.count() -1):
            return
        self.lylic.item(self.lylic.currentRow()).setSelected(False)
        self.lylic.item(self.lylic.currentRow() + 1).setSelected(True)
        self.lylic.setCurrentRow(self.lylic.currentRow() + 1)

    def sendLylic(self):
        if self.lylicNotShow.isChecked():
            return
        result = self.zoom.sendCC(self.lylic.currentItem().text(), 'ko-KR')
        if result == False:
            QMessageBox.information(self, "QMessageBox", "Zoom URL을 설정하세요.")

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
