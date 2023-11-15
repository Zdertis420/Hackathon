import sys

from layout import Setup
from PyQt6.QtWidgets import (QMainWindow,
                             QApplication)


class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        Setup.setupUi(object, MainWindow=MainWin)



app = QApplication(sys.argv)
mainWindow = MainWin()

mainWindow.show()
sys.exit(app.exec())
