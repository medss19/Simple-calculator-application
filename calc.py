import sys
from functools import partial
from math import sqrt, exp, sin, cos, tan, log, e

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QGridLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QFrame
)


stylesheet = """
QMainWindow {
    background-color: #2E2E2E;
}

QLineEdit {
    background-color: #F0F0F0;
    color: #000000;
    border: 2px solid #CCCCCC;
    border-radius: 10px;
    padding: 5px;
    font-size: 18px;
}

QPushButton {
    background-color: #fc94af;
    color: black;
    border: 2px solid black;
    border-radius: 10px;
    padding: 10px;
    font-size: 16px;
    font-weight: bold;
}

QPushButton:pressed {
    background-color: #04BADE;
}

QPushButton#operator {
    background-color: #ffe5f1;
}

QPushButton#trigno {

    background-color: #f5c3c2;
}

QPushButton#operator:pressed {
    background-color: #FF8C00;
}

QPushButton#trigno:pressed {
    background-color: #FFE5D6;
}

QPushButton#clear {
    background-color: #ff1694;
}

QPushButton#clear:pressed {
    background-color: #CC0000;
}

QPushButton#delete {
    background-color: #ff1694;
}

QPushButton#equal {
    background-color: #fc4c4e;
}

QPushButton#delete:pressed {
    background-color: #FF4500;
}
"""


ERROR_MSG = "ERROR"
# WINDOW_SIZE = 330
DISPLAY_HEIGHT = 45
BUTTON_SIZE = 50

class CalcWindow(QMainWindow):

    # main window (GUI or view)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Calculator")
        self.setFixedSize(350, 500)
        self.generalLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        self._createDisplay()
        self._createButtons()

    def _createDisplay(self):
        self.display = QLineEdit()
        self.display.setFixedHeight(DISPLAY_HEIGHT)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.generalLayout.addWidget(self.display)

    def _createButtons(self):
        self.buttonMap = {}
        buttonsLayout = QGridLayout()
        keyBoard = [
            ["sin", "cos", "tan", "log", "ln"],
            ["C", "√", "^", "π", "DEL"],
            ["7", "8", "9", "/", "%"],
            ["4", "5", "6", "*", "("],
            ["1", "2", "3", "-", ")"],
            ["00", "0", ".", "+", "="],
        ]

        for row, keys in enumerate(keyBoard):
            for col, key in enumerate(keys):
                self.buttonMap[key] = QPushButton(key)
                self.buttonMap[key].setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
                adjusted_row = row if row < 2 else row + 1
                buttonsLayout.addWidget(self.buttonMap[key], adjusted_row, col)

                if key in {"+", "-", "*", "/", "√", "^", "%", "(", ")", "π"}:
                    self.buttonMap[key].setObjectName("operator")
                elif key in {"sin", "cos", "tan", "log", "ln"}:
                    self.buttonMap[key].setObjectName("trigno")
                elif key == "C":
                    self.buttonMap[key].setObjectName("clear")
                elif key == "DEL":
                    self.buttonMap[key].setObjectName("delete")
                elif key == "=":
                    self.buttonMap[key].setObjectName("equal")

                buttonsLayout.addWidget(self.buttonMap[key], row, col)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        buttonsLayout.addWidget(line, 2, 0, 1, 5) 

        self.generalLayout.addLayout(buttonsLayout)

    def setDisplayText(self, text):
        self.display.setText(text)
        self.display.setFocus()

    def displayText(self):
        return self.display.text()
    
    def clearDisplay(self):
        self.setDisplayText("")

    def deleteLastChar(self):
        currentText = self.display.text()
        self.setDisplayText(currentText[:-1])


def evaluateExpression(expression):
    try:
        expression = expression.replace("√", "sqrt(")
        expression = expression.replace('^', "**")
        # expression = expression.replace('e^', "exp(")
        expression = expression.replace('π', '3.141592653589793')
        expression = expression.replace("sin", "sin(")
        expression = expression.replace("cos", "cos(")
        expression = expression.replace("tan", "tan(")
        expression = expression.replace("log", "log10(")
        expression = expression.replace("ln", "log(")

        if any(func in expression for func in ["sqrt(", "sin(", "cos(", "tan(", "log10(", "log("]):
            expression += ")"

        result = str(eval(expression, {"sqrt": sqrt, "exp": exp, "sin": sin, "cos": cos, "tan": tan, "log10": log, "log": log, "e": e}, {}))

    except Exception:
        result = ERROR_MSG
    return result

class PyCalc:
    # Controller class

    def __init__(self, model, view):
        self._evaluate = model
        self._view = view
        self._connectSignalsAndSlots()

    def _calculateResult(self):
        result = self._evaluate(expression = self._view.displayText())
        self._view.setDisplayText(result)

    def _buildExpression(self, subExpression):
        if self._view.displayText() == ERROR_MSG:
            self._view.clearDisplay()
        expression = self._view.displayText() + subExpression
        self._view.setDisplayText(expression)

    def _connectSignalsAndSlots(self):
        for keySymbol, button in self._view.buttonMap.items():
            if keySymbol not in {"=", "C", "DEL"}:
                button.clicked.connect(
                    partial(self._buildExpression, keySymbol)
                )
        self._view.buttonMap["="].clicked.connect(self._calculateResult)
        self._view.display.returnPressed.connect(self._calculateResult)
        self._view.buttonMap["C"].clicked.connect(self._view.clearDisplay)
        self._view.buttonMap["DEL"].clicked.connect(self._view.deleteLastChar)

def main() :

    calcApp = QApplication([])
    calcApp.setStyleSheet(stylesheet)
    calcWindow = CalcWindow()
    calcWindow.show()
    PyCalc(model = evaluateExpression, view = calcWindow)
    sys.exit(calcApp.exec())

if __name__ == "__main__":
    main()
