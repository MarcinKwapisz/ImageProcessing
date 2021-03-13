from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1032, 847)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.image = QtWidgets.QLabel(self.centralwidget)
        self.image.setGeometry(QtCore.QRect(0, 0, MainWindow.width(), MainWindow.height()))
        self.image.setText("")
        self.image.setScaledContents(False)
        self.image.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.image.setWordWrap(False)
        self.image.setObjectName("image")
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1032, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuFilters = QtWidgets.QMenu(self.menubar)
        self.menuFilters.setObjectName("menuFilters")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave_As = QtWidgets.QAction(MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionCopy = QtWidgets.QAction(MainWindow)
        self.actionCopy.setObjectName("actionCopy")
        self.actionPaste = QtWidgets.QAction(MainWindow)
        self.actionPaste.setObjectName("actionPaste")
        self.actionZoom_In_25 = QtWidgets.QAction(MainWindow)
        self.actionZoom_In_25.setObjectName("actionZoom_In_25")
        self.actionZoom_Out_25 = QtWidgets.QAction(MainWindow)
        self.actionZoom_Out_25.setObjectName("actionZoom_Out_25")
        self.actionNormal_Size = QtWidgets.QAction(MainWindow)
        self.actionNormal_Size.setObjectName("actionNormal_Size")
        self.actionFit_to_Window = QtWidgets.QAction(MainWindow)
        self.actionFit_to_Window.setObjectName("actionFit_to_Window")
        self.actionTestFilter = QtWidgets.QAction(MainWindow)
        self.actionTestFilter.setObjectName("actionTestFilter")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuView.addAction(self.actionZoom_In_25)
        self.menuView.addAction(self.actionZoom_Out_25)
        self.menuView.addAction(self.actionNormal_Size)
        self.menuView.addAction(self.actionFit_to_Window)
        self.menuFilters.addAction(self.actionTestFilter)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuFilters.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.actionOpen.triggered.connect(lambda: self.loadImageFromFile())
        self.actionZoom_In_25.triggered.connect(lambda: self.zoomInBy25())
        self.actionZoom_Out_25.triggered.connect(lambda: self.zoomOutBy25())
        self.actionFit_to_Window.triggered.connect(lambda: self.fitToWindow())

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.menuFilters.setTitle(_translate("MainWindow", "Filters"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionOpen.setText(_translate("MainWindow", "Open ..."))
        self.actionSave_As.setText(_translate("MainWindow", "Save As ..."))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionCopy.setText(_translate("MainWindow", "Copy"))
        self.actionPaste.setText(_translate("MainWindow", "Paste"))
        self.actionZoom_In_25.setText(_translate("MainWindow", "Zoom In (25%)"))
        self.actionZoom_Out_25.setText(_translate("MainWindow", "Zoom Out (25%)"))
        self.actionNormal_Size.setText(_translate("MainWindow", "Normal Size"))
        self.actionFit_to_Window.setText(_translate("MainWindow", "Fit to Window"))
        self.actionTestFilter.setText(_translate("MainWindow", "TestFilter"))
        self.actionAbout.setText(_translate("MainWindow", "About"))

    def loadImageFromFile(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self.centralwidget, 'Open file', './',
                                                      "Image files (*.pgm *.pbm *.ppm *.png)")
        self.pixmap = QtGui.QPixmap(fname[0])
        self.loadImage()

    def loadImage(self):
        self.image.setPixmap(self.pixmap)

    def zoomInBy25(self):
        self.pixmap = self.pixmap.scaled(int(self.pixmap.width() * 1.25),
                                         int(self.pixmap.height() * 1.25))
        self.loadImage()

    def zoomOutBy25(self):
        self.pixmap = self.pixmap.scaled(int(self.pixmap.width() * 0.75),
                                         int(self.pixmap.height() * 0.75))
        self.loadImage()

    def fitToWindow(self):
        self.image.resize(MainWindow.width(), MainWindow.height())
        self.pixmap = self.pixmap.scaled(MainWindow.width(),
                                         MainWindow.height())
        self.loadImage()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())