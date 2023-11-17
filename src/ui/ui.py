# import gc
# gc.disable()

import os

import sys

from PyQt6.QtWidgets import (QWidget,
                             QApplication,
                             QLineEdit,
                             QPushButton,
                             QCheckBox,
                             QLabel,
                             QFileDialog)


class MainWin(QWidget):
    def __init__(self):
        super().__init__()

        self.heck = 'hack'

        self.setup()

    def toggleSecond(self, state):
        if state == 2:
            self.topicPath.setEnabled(True)
            self.topicBrowse.setEnabled(True)
        else:
            self.topicPath.setEnabled(False)
            self.topicBrowse.setEnabled(False)

    def getTextsPath(self):
        return self.textPath.text()

    def getTopicsPath(self):
        if self.topicPath.isEnabled():
            return self.topicPath.text()

    def getOutputPath(self):
        return self.outputPath.text()

    def browseTextsPath(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setDirectory(r'')
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            filname = dialog.selectedFiles()
            self.textPath.setText(*filname)
        dialog.show()

    def browseTopicsPath(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setDirectory(r'')
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            filname = dialog.selectedFiles()
            self.topicPath.setText(*filname)
        dialog.show()

    def browseOutputsPath(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setDirectory(r'')
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            filname = dialog.selectedFiles()
            self.outputPath.setText(*filname)
        dialog.show()

    def callBack(self):
        print(self.getTextsPath(),
              self.getTopicsPath(),
              self.getOutputPath())

        if self.first.checkState():
            os.system(f'{self.heck} --task 1 -i {self.getTextsPath()} -o {self.getOutputPath()}')
        elif self.second.checkState():
            os.system(
                f'{self.heck} --task 2 -i {self.getTextsPath()} -o {self.getOutputPath()} -t {self.getTopicsPath()}')
        elif self.first.stateChanged() and self.second.stateChanged():
            os.system(
                f'{self.heck} --task 0 -i {self.getTextsPath()} -o {self.getOutputPath()} -t {self.getTopicsPath()}')
        else:
            self.response.setText('Invalid input: You should choose at least one task!')

    def setup(self):
        self.setGeometry(300, 300, 800, 400)
        self.setWindowTitle('Hackathon')

        self.textPath = QLineEdit(self)
        self.textPath.move(40, 40)
        self.textPath.resize(610, 30)

        self.textBrowse = QPushButton(self)
        self.textBrowse.setText('Browse')
        self.textBrowse.move(680, 40)
        self.textBrowse.resize(100, 30)
        self.textBrowse.clicked.connect(self.browseTextsPath)  # YOU KNOW WHAT?? FUCK YOU ITS TOTALLY VALID

        self.topicPath = QLineEdit(self)
        self.topicPath.setEnabled(False)
        self.topicPath.move(40, 100)
        self.topicPath.resize(610, 30)

        self.topicBrowse = QPushButton(self)
        self.topicBrowse.setEnabled(False)
        self.topicBrowse.setText('Browse')
        self.topicBrowse.move(680, 100)
        self.topicBrowse.resize(100, 30)
        self.topicBrowse.clicked.connect(self.browseTopicsPath)

        self.outputPath = QLineEdit(self)
        self.outputPath.move(40, 160)
        self.outputPath.resize(610, 30)

        self.outputBrowse = QPushButton(self)
        self.outputBrowse.setText('Browse')
        self.outputBrowse.move(680, 160)
        self.outputBrowse.resize(100, 30)
        self.outputBrowse.clicked.connect(self.browseOutputsPath)

        self.first = QCheckBox(self)
        self.first.setText('Do first')
        self.first.move(40, 230)
        self.first.resize(70, 40)

        self.second = QCheckBox(self)
        self.second.setText('Do second')
        self.second.move(140, 230)
        self.second.resize(80, 40)
        self.second.stateChanged.connect(self.toggleSecond)  # IVE ALREADY SAID IT! FUCK YOOOOU

        self.start = QPushButton(self)
        self.start.setText('Start')
        self.start.move(250, 235)
        self.start.resize(100, 30)
        self.start.clicked.connect(self.callBack)

        self.response = QLabel(self)
        self.response.setText('')
        self.response.move(40, 300)
        self.response.resize(600, 100)


app = QApplication(sys.argv)
mainWindow = MainWin()

mainWindow.show()
sys.exit(app.exec())
