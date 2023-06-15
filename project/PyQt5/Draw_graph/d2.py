import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

#
# list_box: 1/2/3차함수를 고를 공간 | viewer: 그래프가 그려질 공간 | cal_entry: 식을 적을 공간 |
# draw_btn: 그래프 그리기 버튼

UI = uic.loadUiType('draw_graph.ui')[0]

class Window(QMainWindow,QWidget,UI):
    def __init__(self,*args,**kwargs):
        # 부모 클래스에 대해서도 초기화
        super(Window,self).__init__(*args,**kwargs)
        UI.__init__(self)
        self.setupUi(self)
        # list_box 안에 값 저장하기
        for i in ['1차함수','2차함수','3차함수']:
            self.list_box.addItem(i)

        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot()
        self.ax.spines['bottom'].set_position(('data', 0))  # x축 y축 설정
        self.ax.spines['left'].set_position(('data', 0))
        self.ax.grid(color = '0.8')                         # 회색 격자 무늬 넣기
        self.ax.plot()
        self.addToolBar(NavigationToolbar(self.canvas, self))
        self.layout = self.graph_layout
        self.layout.addWidget(self.canvas)
        # draw graph 버튼 눌렀을때 동작 지정
        self.draw_btn.clicked.connect(self.draw_graph)

    def draw_graph(self):
        self.ax.claer()
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)
        x = np.array(range(-20, 20))
        y = x + 1
        self.ax.plot(x,y)
        self.show()
        print(1)
        # n = int(self.list_box.currentText()[0])
        # ent = self.cal_entry.toPlainText().replace(' ','')
        # X = ['x**3', 'x**2', 'x']
        # nums = []
        # for x in X:
        #     idx = ent.find(x)
        #     if idx >= 0:
        #         num = ent[:idx]
        #         nums.append(1 if num in ['', '+', '-'] else int(num))
        #         ent = ent[idx + len(x):]
        #     else:
        #         nums.append(0)
        # if ent and ent[-1].isdigit():
        #     nums.append(int(ent))
        # else:
        #     nums.append(0)
        # a,b,c,d = nums
        # xrange = np.arange(-20,20)
        # if a:
        #     y = a*x**3+b*x**2+c*x+d
        #     self.ax.plot(xrange,y)
        # elif b:
        #     y = b * x ** 2 + c * x + d
        #     self.ax.plot(xrange,y)
        # elif c:
        #     y = a * x ** 3 + b * x ** 2 + c * x + d
        #     self.ax.plot(xrange,y)







if __name__=='__main__':             # import된 것들을 실행시키지 않고 __main__에서 실행하는 것만 실행 시킨다.
                                     # 즉 import된 다른 함수의 코드를 이 화면에서 실행시키지 않겠다는 의미이다.
    app = QApplication(sys.argv)     # PyQt5로 실행할 파일명을 자동으로 설정, PyQt5에서 자동으로 프로그램 실행
    window = Window()                # Main 클래스 myApp으로 인스턴스화
    window.show()                    # myApp에 있는 ui를 실행한다.
    app.exec_()



# x² x³