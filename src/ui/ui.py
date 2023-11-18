import gc
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

        self.heck = './hack'

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
        dialog.setDirectory(r'/home/main/coding/Hackaton/data/docs')
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            filname = dialog.selectedFiles()
            self.textPath.setText(*filname)
        dialog.show()

    def browseTopicsPath(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setDirectory(r'/home/main/coding/Hackaton/data/themes')
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            filname = dialog.selectedFiles()
            self.topicPath.setText(''.join(filname))
        dialog.show()

    def browseOutputsPath(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setDirectory(r'/home/main/coding/Hackaton/data')
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            filname = dialog.selectedFiles()
            self.outputPath.setText(''.join(filname))
        dialog.show()

    def callBack(self):
        self.trash_q_label = QLabel("Processing... This may take a while")
        # TODO: если os.system вернёт 127 (команда не найдена) - запросить путь к hack
        if self.first.isChecked():
            if os.system(f'{self.heck} --task 1 -i {self.getTextsPath()} -o {self.getOutputPath()}'):
                sys.exit(-1)
        elif self.second.isChecked():
            if os.system( 
                    f'{self.heck} --task 2 -i {self.getTextsPath()} -o {self.getOutputPath()} -t {self.getTopicsPath()}'):
                sys.exit(-1)
        elif self.first.isChecked() and self.second.isChecked():
            if os.system( \
                    f'{self.heck} --task 0 -i {self.getTextsPath()} -o {self.getOutputPath()} -t {self.getTopicsPath()}'):
                sys.exit(-1)
        else:
            self.response.setText('Invalid input: You should choose at least one task!')
        self.trash_q_label.close()
        del self.trash_q_label

    def setup(self):
        self.setGeometry(300, 300, 800, 400)
        self.setWindowTitle('Hackathon')

        self.firstPath = QLabel(self)
        self.firstPath.setText("Texts' path here")
        self.firstPath.move(40, 20)

        self.textPath = QLineEdit(self)
        self.textPath.move(40, 40)
        self.textPath.resize(610, 30)

        self.textBrowse = QPushButton(self)
        self.textBrowse.setText('Browse')
        self.textBrowse.move(680, 40)
        self.textBrowse.resize(100, 30)
        self.textBrowse.clicked.connect(self.browseTextsPath)  # YOU KNOW WHAT?? FUCK YOU ITS TOTALLY VALID

        self.secondPath = QLabel(self)
        self.secondPath.setText("Topics' path here")
        self.secondPath.move(40, 80)

        self.topicPath = QLineEdit(self)
        self.topicPath.setEnabled(False)
        self.topicPath.move(40, 100)
        self.topicPath.resize(610, 30)

        self.topicBrowse = QPushButton(self)
        self.topicBrowse.setEnabled(False)
        self.topicBrowse.setText('Browse')
        self.topicBrowse.move(680, 100)
        self.topicBrowse.resize(100, 30)
        self.topicBrowse.clicked.connect(self.browseTopicsPath)  # stupid bitch

        self.thirdPath = QLabel(self)
        self.thirdPath.setText("Output's path here")
        self.thirdPath.move(40, 140)

        self.outputPath = QLineEdit(self)
        self.outputPath.move(40, 160)
        self.outputPath.resize(610, 30)

        self.outputBrowse = QPushButton(self)
        self.outputBrowse.setText('Browse')
        self.outputBrowse.move(680, 160)
        self.outputBrowse.resize(100, 30)
        self.outputBrowse.clicked.connect(self.browseOutputsPath)  # .....

        self.first = QCheckBox(self)
        self.first.setText('Do first')
        self.first.move(40, 230)
        self.first.resize(70, 40)

        self.second = QCheckBox(self)
        self.second.setText('Do second')
        self.second.move(140, 230)
        self.second.resize(80, 40)
        self.second.stateChanged.connect(self.toggleSecond)  # IVE ALREADY SAID IT! YOU STUPID

        self.start = QPushButton(self)
        self.start.setText('Start')
        self.start.move(250, 235)
        self.start.resize(100, 30)
        self.start.clicked.connect(self.callBack)

        self.response = QLabel(self)
        self.response.setText('')
        self.response.move(40, 250)
        self.response.resize(600, 100)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWin()
    if len(sys.argv) == 2:
        mainWindow.heck = sys.argv[1]
    else:
        print("ЗАПУСК ПРОРГАММЫ: hack-ui <path-to-hack>")
    mainWindow.show()
    sys.exit(app.exec())
