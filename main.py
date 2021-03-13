from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication, QMenu, QAction, QFileDialog,QLabel,QWidget,QInputDialog
from PyQt5.QtGui import QIcon

import image
import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.image = image.Images()
        self.pixmap = self.image.toPixmap()
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
        self.label.setPixmap(self.pixmap)
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

    def createTollbar(self):
        scaleUpAct = QAction(QIcon('zoomin.png'),'Scale up', self)
        undoAct = QAction(QIcon('undo.png'),'Undo', self)
        scaleDownAct = QAction(QIcon('zoomout.png'),'Scale down', self)
        scaleUpAct.triggered.connect(self.scaleup)
        undoAct.triggered.connect(self.undo)
        scaleDownAct.triggered.connect(self.scaledown)
        self.toolbar = self.addToolBar("Scale")
        self.toolbar.addAction(scaleUpAct)
        self.toolbar.addAction(scaleDownAct)
        self.toolbar.addAction(undoAct)



    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def save(self):
        print(1223)

    def open(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file', './',"Image files (*.pgm *.pbm *.ppm *.png)")
        self.image.imageLoader(filename[0])
        self.refresh()

    def undo(self):
        self.image.undo()
        self.refresh()

    def refresh(self):
        self.pixmap = self.image.toPixmap()
        self.label.setPixmap(self.pixmap)

    def scaleup(self):
        self.pixmap = self.pixmap.scaled(int(self.pixmap.width() * 1.1), int(self.pixmap.height() * 1.1),QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(self.pixmap)

    def scaledown(self):
        self.pixmap = self.pixmap.scaled(int(self.pixmap.width() * 0.9), int(self.pixmap.height() * 0.9),QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(self.pixmap)

    def saturate(self):
        ratio, pressed = QInputDialog.getDouble(self, "Set value","Value:", 0, 0, 5, 2)
        if pressed:
            self.image.saturation(ratio)
            self.refresh()





def main():

    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()