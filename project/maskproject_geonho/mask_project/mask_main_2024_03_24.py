import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import PIL
from PIL import ImageTk, Image
from mask_api_2024_03_24 import *

window = tk.Tk()                    # 메인 창
window.title("미세먼지 마스크")        # 프로그램 타이틀
window.geometry("440x220+100+100")  # geometry("가로x세로+x좌표+y좌표") : 해당 크기, 좌표에 창 최초 생성
window.resizable(False,False)       # resizable(True,False): 창의 크기를 변경시킬 지 정해주는 내용(True: 가능, False: 불가능),

# TODO: 0. 지역 구분하기
Frame1 = tk.Frame(window, relief="solid", bd=1,width=250,height=130)
Frame1.place(x = 10,y = 10)

Frame2 = tk.Frame(window,relief="solid",bd=1)
Frame2.place(x=260,y=10,width=160 ,height=130)

Frame3 = tk.Frame(window, relief="solid", bd=1,width=410,height=70)
Frame3.place(x = 10,y = 140)


# TODO: 1. 지역선택할 수 있는 버튼(버튼 클릭시, 각 지역들(선택지)가 나오고 클릭하면 해당 선택지가 결정이 되는 형태)
area = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주']
area_box = ttk.Combobox(Frame1,values=area)
area_box.place(x = 15, y = 5, width = 130,height = 30)
area_box.set("지역을 선택하시오.")

# TODO: 2. 미세먼지, 초미세먼지, 질병 감염 수치 증가폭등의 데이터를 표현할 공간(TEXT, 버튼 클릭시 데이터 표현, 기본은 주제에 대해서만 )
pm10_label = tk.Label(Frame2, text="미세먼지: ",relief='solid',bd=1,anchor='w',padx=5)
pm10_label.place(x=5,y=10,width=140,height= 30)

pm25_label = tk.Label(Frame2, text="초미세먼지: ",relief='solid',bd=1,anchor='w',padx=5)
pm25_label.place(x=5,y=50,width=140,height= 30)

disease_label= tk.Label(Frame2, text="질병수치(감기): ",relief='solid',bd=1,anchor='w',padx=5)
disease_label.place(x=5,y=90,width=140,height= 30)

# TODO: 3. 미세먼지, 초미세먼지 기준표를 담아줄 공간(TEXT)
pm_standard = """
미세먼지: 0~30(좋음) 31~80(보통) 81~150(나쁨) 151이상(매우나쁨)
초미세먼지: 0~15(좋음) 16~50(보통) 51~100(나쁨) 101이상(매우나쁨)
질병수치(감기): 1(좋음) 2(보통) 3(나쁨) 4(매우나쁨)"""
pm_standard_label = tk.Label(Frame3, text=pm_standard, anchor='w')
pm_standard_label.place(x = 0,y = 0)

# TODO: 4. 마스크 이미지를 보여줄 공간
mask_label = tk.Label(Frame1,background='white')
mask_label.place(x = 15,y = 40, width = 210, height = 80)

# TODO: 5. 결과값 보여주기 활성화 버튼
btn_play = tk.Button(Frame1, text="실행")
btn_play.place(x = 155, y = 5, width = 70, height=30)

def show_mask():
    """
    1.combobox에서 선택한 지역을 가지고 온다.
    2.가지고 온 지역값을 get_pm()에 전달하면서 실행
    3.가지고 온 지역값을 get_disease()에 전달하면서 실행
    4. get_pm()으로 가져온 미세먼지 초 미세먼지 데이터와, get_disease()로 가져온 질병 데이터로
    평균 수치를 내 4 단계로 구분한 값을 가지고 온다.
    5. 해당 값을 mask_image를 불러오는데 사용
    그 이후는 아래 코드 그대로 사용 + 미세먼지, 초미세먼지, 질병데이터를 각 label에 붙여주기
    :return:
    """
    area_data = area_box.get()  # 선택한 지역
    # print(area_data,type(area_data))
    if area_data == "지역을 선택하시오.":
        msgbox.showwarning('경고','지역을 선택하고 실행해주세요.')
        return

    pm10, pm25 = get_pm(area_data)   # 미세먼지, 초미세먼지 수치값
    disease = get_disease(area_data) # 감기 질병 데이터
    # print(pm10,pm25,disease)
    avg = get_avg(pm10,pm25,disease)
    # print(avg)

    # 마스크 이미지 불러오기 + 사이즈 맞추기
    mask_image = Image.open(f'mask_{avg}.png')
    resized_image = mask_image.resize((210, 80))
    img = ImageTk.PhotoImage(resized_image)
    mask_label.config(image=img)
    mask_label.image = img

    # 미세먼지, 초미세먼지, 질병 데이터 라벨에 등록
    pm10_label.config(text = f"미세먼지: {pm10}")
    pm25_label.config(text = f"초미세먼지: {pm25}")
    disease_label.config(text = f"질병수치(감기): {disease}")

btn_play.config(command = show_mask)

window.mainloop()  # 프로그램을 종료될때까지 유지
