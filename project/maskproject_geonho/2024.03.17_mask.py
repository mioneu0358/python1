import tkinter as tk
import PIL
from PIL import ImageTk, Image
window = tk.Tk()                    # 메인 창
window.title("미세먼지 마스크")       # 프로그램 타이틀
window.geometry("400x200+100+100")  # geometry("가로x세로+x좌표+y좌표") : 해당 크기, 좌표에 창 최초 생성
window.resizable(True,True)       # resizable(True,False): 창의 크기를 변경시킬 지 정해주는 내용(True: 가능, False: 불가능),

# TODO: 0. 지역 구분하기
frame1 = tk.Frame(window, relief="solid", bd=1,width=400,height=130)
frame1.pack(side = "top")

frame2 = tk.Frame(window, relief="solid", bd=1,width=400,height=70)
frame2.pack(side="bottom")

frame3 = tk.Frame(frame1,relief="solid",bd=1)
frame3.place(x=250,y=0,width=150 ,height=130)


# TODO: 1. 지역선택할 수 있는 버튼(버튼 클릭시, 각 지역들(선택지)가 나오고 클릭하면 해당 선택지가 결정이 되는 형태)


# TODO: 2. 미세먼지, 초미세먼지, 질병 감염 수치 증가폭등의 데이터를 표현할 공간(TEXT, 버튼 클릭시 데이터 표현, 기본은 주제에 대해서만 )
pm10_label = tk.Label(frame3, text="미세먼지: ",relief='solid',bd=1,anchor='w',padx=5)
pm10_label.place(x=5,y=10,width=140,height= 30)

pm25_label = tk.Label(frame3, text="초미세먼지: ",relief='solid',bd=1,anchor='w',padx=5)
pm25_label.place(x=5,y=50,width=140,height= 30)

disease_label= tk.Label(frame3, text="질병수치: ",relief='solid',bd=1,anchor='w',padx=5)
disease_label.place(x=5,y=90,width=140,height= 30)

# TODO: 3. 미세먼지, 초미세먼지 기준표를 담아줄 공간(TEXT)
pm_standard = """
미세먼지: 0~30(좋음) 31~80(보통) 81~150(나쁨) 151이상(매우나쁨)
초미세먼지: 0~15(좋음) 16~50(보통) 51~100(나쁨) 101이상(매우나쁨)
"""
pm_standard_label = tk.Label(frame2, text=pm_standard)
pm_standard_label.pack()
# TODO: 4. 마스크 이미지를 보여줄 공간

# TODO: 5. 결과값 보여주기 활성화 버튼
window.mainloop()  # 프로그램을 종료될때까지 유지
