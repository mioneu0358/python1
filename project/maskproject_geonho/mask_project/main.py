from PyQt5.QtWidgets import QMainWindow, QWidget,QLabel,QDateTimeEdit, QVBoxLayout, QApplication
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
import sys
from apis import get_api
form_class = uic.loadUiType("masked_ui.ui")[0]

class WindowClass(QMainWindow,form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_show_mask.clicked.connect(self.get_image)
        self.pm10, self.pm25 = get_api()

    def get_image(self):
        avg = self.get_avg(self.pm10,self.pm25)

        print(self.pm10,self.pm25,avg)
        self.qPixmapVar = QPixmap()
        self.qPixmapVar.load(f"mask_{avg}.png")
        self.qPixmapVar = self.qPixmapVar.scaledToWidth(250)
        self.mask_label.setPixmap(self.qPixmapVar)
        self.pm10_label.setText(f"미세먼지 농도: {self.pm10}")
        self.pm25_label.setText(f"초 미세먼지 농도: {self.pm25}")

    def get_avg(self,pm10,pm25):
        # pm10(미세먼지) 수치별 기준: 0 ~ 80: 좋음, 80~150: 약간 나쁨,  150~ 300: 주의보(나쁨), 300~: 경보(매우 나쁨)
        p10,p25 = 4,4
        pm10_std = [80,150,300]
        # pm2.5(초미세먼지) 수치별 기준:0~ 40: 좋음, 40~ 75: 약간 나쁨,  75~150: 주의보(나쁨),  150~ 경보(매우나쁨)
        pm25_std = [40,75,150]
        for i in range(3):
            if pm10 < pm10_std[i]:
                p10 = i + 1
                break
        for i in range(3):
            if pm25 < pm25_std[i]:
                p25 = i + 1
                break
        return (p10 + p25) // 2

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WindowClass()
    window.show()
    app.exec_()