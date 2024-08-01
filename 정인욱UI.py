from tkinter import *
from tkinter.font import Font
class MyWindow(Tk):

    def __init__(self):
        super().__init__()
        # self.resizable(False,False)
        self.geometry('680x420+100+100')
        label_font = Font(family="맑은 고딕", size=12)
        entry_font = Font(family="맑은 고딕", size=15)
        self.setting_text = Label(self,text='설정',relief='flat',bd=1)
        self.setting_text.place(x=10,y=10,width=40,height=20)
        self.input_frame1 = Frame(self,relief="sunken",bd=3)
        self.input_frame1.place(x=10,y=30,width=618,height=45)

        # 질량 입력
        self.mass_entry = Entry(self.input_frame1, bd=2,font = label_font)

        # 회전운동 선택
        self.rotation_check = Checkbutton(self.input_frame1,text="회전운동",relief="raised", font=entry_font)
        self.rotation_check.place(x=0,y=0,width=120,height=40)
        #
        temp1 = Label(self.input_frame1,relief='sunken', bd=1)
        temp1.place(x=120, y=0, width=30, height=40)

        # # 마찰력 입력
        self.friction_label = Label(self.input_frame1,text="마찰력",relief='raised',bd=2, font=label_font)
        self.friction_label.place(x=150,y=0,width=60,height=40)
        self.friction_entry = Entry(self.input_frame1,font=entry_font,bd=2, justify='center')
        self.friction_entry.place(x=210, y=0, width=120, height=40)

        temp1 = Label(self.input_frame1,relief='sunken', bd=1)
        temp1.place(x=120, y=0, width=30, height=40)

        # # 시간 입력
        self.time_label = Label(self.input_frame1,text='시간(초)',relief='raised',bd=2, font=label_font,)
        self.time_label.place(x=360,y=0,width=80,height=40)
        self.time_entry = Entry(self.input_frame1,font=entry_font,bd=2, justify='center')
        self.time_entry.place(x=440,y=0, width=100,height=40)

        #
        # # 낙하방식(자유낙하/빗면 선택)
        # self.output_frame = Frame(self,relief="solid",bd=2)
        # self.output_frame.place(x=10, y=140, width=618, height=275)

        # 빗면의 높이
        self.hypotenuse_height_label = Label(self)
        # 빗면의 각도
        self.hypotenuse_height_angle = Label(self)
        # 물체의 모양

        # 주는 힘의 크기

# 1. 질량 입력
# 2. 회전운동 O/X 선택
#     회전운동한다면:
#         3.마찰력 입력 0 ~ x
#         마찰력이 0이라면:
#             4. 총 걸리는 시간 입력
#                 총걸리는 시간이 -1이라면:
#                     5. 자유낙하/빗면 선택
#                         자유낙하라면:
#                             6. 높이 물어보고 속도 계산
#                         빗면이라면:
#                             6. 빗면의 높이와 각도를 물어보고 나중 속도 계산
#                 총 걸리는 시간이 -1이 아니라면:

#         마찰력이 있다면:
#             마찰력 공식을 이용하여 위의 4,5,6 수행
#   회전 운동하지 않는다면:
#       3. 물체 모양 선택(속이 빈 구, 구, ...)
#            속이 빈 구라면
#               4. 상황 선택(빗면, 수평면,...)
#                    빗면이라면:
#                         마찰력, 높이, 각도등을 입력 후, 빗면에서 내려간 후의 병진운동 속도와 각속도 출력
#                    수평면이라면:
#                         마찰력, 주는 힘의 크기, 걸리는 시간 등을 입력 후 병진운동 속도와 각속도를 출력
#





if __name__ == "__main__":
    app = MyWindow()
    app.mainloop()
