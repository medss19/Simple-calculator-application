import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget

WINDOW_SIZE = 235

class CalcWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Calculator")
        self.setFixedSize(WINDOW_SIZE, WINDOW_SIZE)
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

def main() :

    calcApp = QApplication([])
    calcWindow = CalcWindow()
    calcWindow.show()
    sys.exit(calcApp.exec())

if __name__ == "__main__":
    main()
