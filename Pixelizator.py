import sys

from PIL import Image
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import shutil

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        loadUi("MainWindow.ui", self)
        self.settings.clicked.connect(lambda: MainWindow.change(self, 1))
        self.settingsHome.clicked.connect(lambda: MainWindow.change(self, 0))
        self.show()

    def change(self, i):
        self.pages.setCurrentIndex(i)

    def init_ui(self):
        self.pixelizationLevelSlider.valueChanged[int].connect(self.changeValue)
        self.chooseBtn.clicked.connect(self.showDialog)

    def changeValue(self, value):
        # slider from 1 to 350
        img = Image.open('alg-img/algimg.jpg')
        width, height = img.size

        slider = value
        scalew = int((width / 1000) * slider)
        scaleh = int((height / 1000) * slider)

        # if user choose little picture
        if scalew <= 0:
            scalew = 1
        if scaleh <= 0:
            scaleh = 1

        # Resize smoothly down to scalew x scaleh pixels
        imgSmall = img.resize((scalew, scaleh), resample=Image.BILINEAR)

        result = imgSmall.resize(img.size, Image.NEAREST)  # Scale back up using NEAREST to original size
        result.save('alg-img/result.png')  # Save on jpg or png
        self.changeScale()

    def resizeEvent(self, event):
        self.changeScale()

    def changeScale(self):
        pix = QPixmap('alg-img/result.png')
        pix = pix.scaled(self.imageWindow.size(), Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
        self.imageWindow.setPixmap(pix)

    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Image files (*.jpg *.png)")[0]
        # if button close pushed
        if fname != '':
            shutil.copyfile(fname, r'alg-img/algimg.jpg')
            self.showPic()

    def showPic(self):
        img = Image.open('alg-img/algimg.jpg')
        width, height = img.size

        slider = 100
        scalew = int((width / 1000) * slider)
        scaleh = int((height / 1000) * slider)

        # Resize smoothly down to scalew x scaleh pixels
        imgSmall = img.resize((scalew, scaleh), resample=Image.BILINEAR)

        result = imgSmall.resize(img.size, Image.NEAREST)  # Scale back up using NEAREST to original size
        result.save('alg-img/result.png')  # Save on jpg or png
        self.changeScale()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.init_ui()
    app.exec_()


if __name__ == '__main__':
    main()
