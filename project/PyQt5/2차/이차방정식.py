from sympy import init_printing, exp
import math
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

form_class = uic.loadUiType("이차방정식.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setGeometry(100,50,740,300)
        self.setupUi(self)
        self.button_cal.clicked.connect(self.get_result)
        self.button_graph.clicked.connect(self.get_graph)
        self.graphDialog = QDialog(self)
        self.graphCheck = False

    def func(self):
        self.label_result.setText('결과값 변경')

    def calculate(self):
        # 사용자로부터 a, b, c 값을 입력받습니다.
        a,b,c = self.line_a.text(), self.line_b.text(), self.line_c.text()
        try:
            a,b,c = int(a),int(b),int(c)
        except ValueError:
            return "계수 a,b,c,는 숫자여야 합니다."
        if a == 0 :
            return 'a는 0일 수 없습니다.'
        a,b,c = int(a),int(b),int(c)
        # 판별식을 계산합니다.
        discriminant = b**2 - 4*a*c

        # 판별식의 값에 따라 해를 구합니다.
        if discriminant > 0:
            # 두 개의 실근이 있는 경우
            x1 = (-b + math.sqrt(discriminant)) / (2*a)
            x2 = (-b - math.sqrt(discriminant)) / (2*a)
            print(f"해는 두 개의 실근이 있습니다.\nx1 = {x1}, x2 = {x2}")
            return f"해는 두 개의 실근이 있습니다.\nx1 = {x1}, x2 = {x2}"
        elif discriminant == 0:
            # 중근인 경우
            x1 = -b / (2*a)
            print(f"해는 중근입니다: x1 = {x1}")
            return f"해는 중근입니다: x1 = {x1}"
        else:
            # 허근인 경우
            realPart = -b / (2*a)
            imaginaryPart = math.sqrt(-discriminant) / (2*a)
            print(f"해는 두 개의 허근입니다.\nx1 = {realPart} + {imaginaryPart}i, x2 = {realPart} - {imaginaryPart}i")
            return f"해는 두 개의 허근입니다.\nx1 = {realPart} + {imaginaryPart}i, x2 = {realPart} - {imaginaryPart}i"

    def get_result(self):
        result = self.calculate()
        self.label_result.setText(result)

    def get_graph(self):
        if not self.graphCheck:
            self.graphCheck = True
            g = self.geometry()
            self.setGeometry(g.x(),g.y(),g.width(),g.height() + 400)
            self.fig = plt.Figure()
            self.canvas = FigureCanvas(self.fig)

            leftLayout = QVBoxLayout()
            leftLayout.addWidget(self.canvas)

        return


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    # 프로그램 화면을 보여주는 코드
    myWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()