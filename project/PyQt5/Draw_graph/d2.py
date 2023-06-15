import sys
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

# draw_btn: 그래프 그리기 버튼 | graph_layout: 그래프가 그려질 공간 | cal_entry: 식을 적을 공간 |

# 만들어놓은 UI 가져오기
UI = uic.loadUiType('draw_graph.ui')[0]

class Window(QMainWindow,QWidget,UI):
    def __init__(self,*args,**kwargs):
        # 부모 클래스 초기화
        super(Window,self).__init__(*args,**kwargs)
        UI.__init__(self)
        self.setupUi(self)

        # # 그래프 창 이식하기
        self.fig = plt.Figure()                              # 도화지 창
        self.canvas = FigureCanvas(self.fig)                 # 사용할 도화지
        self.toolbar = NavigationToolbar(self.canvas, self)  # graph toolbar
        self.ax = self.fig.add_subplot(111)
        self.layout = self.graph_layout                     # 그래프를 그릴 창
        self.layout.addWidget(self.canvas)                  # 도화지 이식
        self.layout.addWidget(self.toolbar)                 # 툴바 이식
        self.setup_graph()                                  # 그래프 설정값 세팅
        self.ax.plot()                                      # 그리기
        # draw graph 버튼 눌렀을때 동작 지정
        self.draw_btn.clicked.connect(self.draw_graph)

    # 공통된 그래프 설정값
    def setup_graph(self):
        self.ax.clear()
        self.ax.spines['bottom'].set_position(('data', 0))  # x축 y축 설정
        self.ax.spines['left'].set_position(('data', 0))
        self.ax.spines['top'].set_position(('data', 0))  # x축 y축 설정
        self.ax.spines['right'].set_position(('data', 0))
        self.ax.grid(color='0.8')

    # 입력한 식 평가하기
    def Evaluate(self):
        ent = self.cal_entry.toPlainText().replace(' ', '')
        nPower = ['x**3', 'x**2', 'x']
        nums = []
        for n in nPower:
            idx = ent.find(n)
            if idx >= 0:
                num = ent[:idx]
                if num == '':
                    num = 1
                elif num == '-':
                    num = -1
                else:
                    num = int(num)
                nums.append(num)
                ent = ent[idx + len(n):]
            else:
                nums.append(0)
        if ent and ent[-1].isdigit():
            nums.append(int(ent))
        else:
            nums.append(0)
        return nums


    # 새로운 그래프 그리는 함수
    def draw_graph(self):
        abcd=[a,b,c,d] = self.Evaluate()
        if abcd == [0,0,0,0]:
            QMessageBox.warning(self,'수식오류','잘못된 수식입니다.')
            return
        x_ = ['x³','x²','x']
        self.setup_graph()
        x = np.arange(-10,10)
        y = a * x ** 3 + b * x ** 2 + c * x + d

        # 라벨 만들기
        Label = ''
        for i in range(len(x_)):
            if abcd[i] != 0:
                if abs(abcd[i]) == 1:
                    Label += f"+{x_[i]}" if abcd[i] > 0 else f"-{x_[i]}"
                else:
                    Label += f"+{abcd[i]}{x_[i]}" if abcd[i] > 0 else f"-{abcd[i]}{x_[i]}"
        if d:
            Label += f"+{d}" if d > 0 else f"-{d}"

        # 새로 그린 그래프 이식
        self.ax.plot(x,y,label = Label)
        self.ax.legend()
        self.canvas.draw()


if __name__=='__main__':             # import된 것들을 실행시키지 않고 __main__에서 실행하는 것만 실행 시킨다.
                                     # 즉 import된 다른 함수의 코드를 이 화면에서 실행시키지 않겠다는 의미이다.
    app = QApplication(sys.argv)     # PyQt5로 실행할 파일명을 자동으로 설정, PyQt5에서 자동으로 프로그램 실행
    window = Window()                # Main 클래스 myApp으로 인스턴스화
    window.show()
    app.exec_()


# -3x**3+2x**2-x+1
# -x**3+2x
# x**2-1
# 1
