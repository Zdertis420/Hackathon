import sys

from PyQt6.QtWidgets import QMainWindow, QApplication


class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hackathon")
        self.setGeometry(710, 300, 500, 500)


app = QApplication(sys.argv)
mainWindow = MainWin()

mainWindow.show()
sys.exit(app.exec())
