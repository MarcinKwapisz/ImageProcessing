from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication, QMenu, QAction, QFileDialog,QLabel,QWidget,QInputDialog
from PyQt5.QtGui import QIcon

import image
import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.image = image.Images()
        self.pixmap = ''
        self.initUI()

    def initUI(self):
        self.resize(1200, 800)  #set size of window
        self.center()
        self.setWindowTitle('Image Processing')
        self.createWindowLabel()
        self.createMenu()
        self.createTollbar()
        self.show()

    def createWindowLabel(self):
        self.workspace = QWidget(self)
        self.label = QLabel(self.workspace)
        self.label.setGeometry(0, 0, self.width(), self.height())
        self.label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label.setScaledContents(False)
        self.label.setWordWrap(True)
        self.setCentralWidget(self.workspace)

    def createMenu(self):
        menubar = self.menuBar()
        #File menu
        fileMenu = menubar.addMenu('File')
        openAct = QAction('Open', self)
        openAct.triggered.connect(self.open)
        fileMenu.addAction(openAct)
        saveAct = QAction('save', self)
        saveAct.triggered.connect(self.save)
        fileMenu.addAction(saveAct)
        #Filters menu
        filtersMenu = menubar.addMenu('Filters')
        saturateAct = QAction('Saturation', self)
        saturateAct.triggered.connect(self.saturate)
        filtersMenu.addAction(saturateAct)
        brightnessAct = QAction('Brightness', self)
        brightnessAct.triggered.connect(self.light)
        filtersMenu.addAction(brightnessAct)
        invertAct = QAction('Invert', self)
        invertAct.triggered.connect(self.invert)
        filtersMenu.addAction(invertAct)
        monochromaticAct = QAction('Monochromatic', self)
        monochromaticAct.triggered.connect(self.monochromatic)
        filtersMenu.addAction(monochromaticAct)
        monochromatic2Act = QAction('Monochromatic2', self)
        monochromatic2Act.triggered.connect(self.monochromatic2)
        filtersMenu.addAction(monochromatic2Act)
        #Filters own menu
        filtersMenuown = menubar.addMenu('Filters own')
        saturateActown = QAction('Saturation', self)
        saturateActown.triggered.connect(self.saturateOwn)
        filtersMenuown.addAction(saturateActown)
        brightnessActown = QAction('Brightness', self)
        brightnessActown.triggered.connect(self.lightOwn)
        filtersMenuown.addAction(brightnessActown)
        contrast = filtersMenuown.addMenu('&Contrast')
        linearContrastActown = QAction('Linear Contrast', self)
        linearContrastActown.triggered.connect(self.linearContrastOwn)
        contrast.addAction(linearContrastActown)
        LogContrastActown = QAction('Log Contrast', self)
        LogContrastActown.triggered.connect(self.logContrastOwn)
        contrast.addAction(LogContrastActown)
        powerContrastActown = QAction('Power Contrast', self)
        powerContrastActown.triggered.connect(self.powerContrastOwn)
        contrast.addAction(powerContrastActown)
        invertActown = QAction('Invert', self)
        invertActown.triggered.connect(self.invertOwn)
        filtersMenuown.addAction(invertActown)
        monochromaticActown = QAction('Monochromatic', self)
        monochromaticActown.triggered.connect(self.monochromaticOwn)
        filtersMenuown.addAction(monochromaticActown)
        onPixels = filtersMenuown.addMenu('&On Pixels')
        incActown = QAction('Increase', self)
        incActown.triggered.connect(self.incOwn)
        onPixels.addAction(incActown)
        decActown = QAction('Decrease', self)
        decActown.triggered.connect(self.decOwn)
        onPixels.addAction(decActown)
        mulActown = QAction('Multiply', self)
        mulActown.triggered.connect(self.mulOwn)
        onPixels.addAction(mulActown)
        # filtersMenuown.addAction(mulActown)

    def createTollbar(self):
        scaleUpAct = QAction(QIcon('zoomin.png'),'Scale up', self)
        undoAct = QAction(QIcon('undo.png'),'Undo', self)
        forwardAct = QAction(QIcon('forward.png'),'Forward', self)
        scaleDownAct = QAction(QIcon('zoomout.png'),'Scale down', self)
        scaleUpAct.triggered.connect(self.scaleup)
        undoAct.triggered.connect(self.undo)
        forwardAct.triggered.connect(self.forward)
        scaleDownAct.triggered.connect(self.scaledown)
        self.toolbar = self.addToolBar("Scale")
        self.toolbar.addAction(scaleUpAct)
        self.toolbar.addAction(scaleDownAct)
        self.toolbar.addAction(undoAct)
        self.toolbar.addAction(forwardAct)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def save(self):
        filename = QFileDialog.getSaveFileName(self, 'Open file', './',"PGM (*.pgm);;PBM (*pbm);;PPM (*.ppm);;PNG (*.png)")
        if filename[0]:
            self.image.saves(filename)

    def open(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file', './', "Image files (*.pgm *.pbm *.ppm *.png)")
        if filename[0]:
            self.image.imageLoader(filename[0])
            self.refresh()

    def undo(self):
        if self.image.checkIfEmpty():
            self.image.undo()
            self.refresh()

    def forward(self):
        if self.image.checkIfEmpty():
            self.image.forward()
            self.refresh()

    def refresh(self):
        if self.image.checkIfEmpty():
            self.pixmap = self.image.toPixmap()
            self.label.setPixmap(self.pixmap)

    def scaleup(self):
        if self.image.checkIfEmpty():
            self.pixmap = self.pixmap.scaled(int(self.pixmap.width() * 1.1), int(self.pixmap.height() * 1.1),QtCore.Qt.KeepAspectRatio)
            self.label.setPixmap(self.pixmap)

    def scaledown(self):
        if self.image.checkIfEmpty():
            self.pixmap = self.pixmap.scaled(int(self.pixmap.width() * 0.9), int(self.pixmap.height() * 0.9),QtCore.Qt.KeepAspectRatio)
            self.label.setPixmap(self.pixmap)

    def saturate(self):
        if self.image.checkIfEmpty():
            ratio, pressed = QInputDialog.getDouble(self, "Set saturation procentage","Value(0 to 200):", 100, 0, 200, 2)
            if pressed:
                self.image.saturation(ratio/100)
                self.refresh()

    def light(self):
        if self.image.checkIfEmpty():
            ratio, pressed = QInputDialog.getDouble(self, "Set light procentage","Value(0 to 200):", 100, 0, 200, 2)
            if pressed:
                self.image.light(ratio/100)
                self.refresh()

    def invert(self):
        if self.image.checkIfEmpty():
            self.image.invert()
            self.refresh()

    def monochromatic(self):
        if self.image.checkIfEmpty():
            self.image.monochromatic()
            self.refresh()


    def monochromatic2(self):
        if self.image.checkIfEmpty():
            self.image.monochromatic2()
            self.refresh()
#own
    def saturateOwn(self):
        if self.image.checkIfEmpty():
            ratio, pressed = QInputDialog.getDouble(self, "Set saturation procentage","Value(0 to 200):", 100, 0, 200, 0)
            if pressed:
                self.image.saturationOwn(ratio/100)
                self.refresh()

    def lightOwn(self):
        if self.image.checkIfEmpty():
            ratio, pressed = QInputDialog.getDouble(self, "Set light procentage","Value(0 to 200):", 100, 0, 200, 0)
            if pressed:
                self.image.lightOwn(ratio/100)
                self.refresh()

    def linearContrastOwn(self):
        if self.image.checkIfEmpty():
            ratio, pressed = QInputDialog.getDouble(self, "Set contrast procentage","Value(-255 to 255):", 0, -255, 255, 2)
            if pressed:
                self.image.linearcontrastOwn(ratio)
                self.refresh()

    def logContrastOwn(self):
        if self.image.checkIfEmpty():
            ratio, pressed = QInputDialog.getDouble(self, "Set contrast procentage", "Value(0 to 255):", 128, 0, 255, 0)
            if pressed:
                self.image.logcontrastOwn(1+ratio/3)
                self.refresh()

    def powerContrastOwn(self):
        if self.image.checkIfEmpty():
            ratio, pressed = QInputDialog.getDouble(self, "Set contrast procentage", "Value(0 to 200):", 100, 0, 200, 0)
            if pressed:
                self.image.powercontrastOwn(ratio)
                self.refresh()

    def invertOwn(self):
        if self.image.checkIfEmpty():
            self.image.invertOwn()
            self.refresh()

    def monochromaticOwn(self):
        if self.image.checkIfEmpty():
            self.image.monochromaticOwn()
            self.refresh()


    def monochromatic2Own(self):
        if self.image.checkIfEmpty():
            self.image.monochromatic2Own()
            self.refresh()

    def incOwn(self):#increase pixel value
        if self.image.checkIfEmpty():
            ratio, pressed = QInputDialog.getDouble(self, "Set increase value", "Value(0 to 255):", 0, 0, 255, 0)
            if pressed:
                self.image.incOwn(ratio)
                self.refresh()
    def decOwn(self):#decrease pixel value
        if self.image.checkIfEmpty():
            ratio, pressed = QInputDialog.getDouble(self, "Set decrease value", "Value(0 to 255):", 0, 0, 255, 0)
            if pressed:
                self.image.decOwn(ratio)
                self.refresh()
    def mulOwn(self):#multiply pixel value
        if self.image.checkIfEmpty():
            ratio, pressed = QInputDialog.getDouble(self, "Set multiply value", "Value(1 to 255):", 0, 1, 255, 2)
            if pressed:
                self.image.mulOwn(ratio)
                self.refresh()




def main():

    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()