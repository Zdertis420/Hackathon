from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import (QWidget,
                             QHBoxLayout,
                             QTextEdit,
                             QPushButton,
                             QCheckBox,
                             QLabel,
                             QMenuBar,
                             QStatusBar)


class Setup(QWidget):
    def setupUi(self, MainWindow: object):
        self.horizontalLayoutWidget = QWidget()
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(40, 30, 721, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.getPathLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.getPathLayout.setContentsMargins(0, 0, 0, 0)
        self.getPathLayout.setObjectName("getPathLayout")
        self.getPath = QTextEdit(parent=self.horizontalLayoutWidget)
        self.getPath.setEnabled(True)
        self.getPath.setObjectName("getPath")
        self.getPathLayout.addWidget(self.getPath)
        self.Browse = QPushButton(parent=self.horizontalLayoutWidget)
        self.Browse.setObjectName("Browse")
        self.getPathLayout.addWidget(self.Browse)
        self.horizontalLayoutWidget_2 = QWidget()
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(39, 120, 421, 71))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.first = QCheckBox(parent=self.horizontalLayoutWidget_2)
        self.first.setObjectName("first")
        self.horizontalLayout.addWidget(self.first)
        self.second = QCheckBox(parent=self.horizontalLayoutWidget_2)
        self.second.setObjectName("second")
        self.horizontalLayout.addWidget(self.second)
        self.both = QCheckBox(parent=self.horizontalLayoutWidget_2)
        self.both.setIconSize(QtCore.QSize(16, 16))
        self.both.setChecked(False)
        self.both.setObjectName("both")
        self.horizontalLayout.addWidget(self.both)
        self.start = QPushButton(parent=self.horizontalLayoutWidget_2)
        self.start.setObjectName("start")
        self.horizontalLayout.addWidget(self.start)
        self.response = QLabel()
        self.response.setGeometry(QtCore.QRect(50, 320, 191, 81))
        self.response.setText("")
        self.response.setObjectName("response")
        self.menubar = QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.statusbar = QStatusBar()
        self.statusbar.setObjectName("statusbar")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Hackathon"))
        self.Browse.setText(_translate("MainWindow", "Browse"))
        self.first.setText(_translate("MainWindow", "Do only first"))
        self.second.setText(_translate("MainWindow", "Do only seocnd"))
        self.both.setText(_translate("MainWindow", "Do both"))
        self.start.setText(_translate("MainWindow", "Start"))
