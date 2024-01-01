import tkinter as tk
import tkinter.font

window = tk.Tk()

window.title("baseball game")
window.geometry("640x400+100+100")
window.resizable(False,False)
FONT = tk.font.Font(family="궁서체", size = 50)
LISTBOX_FONT = tk.font.Font(family="궁서체", size=20)

mainFrame = tk.Frame(window, width=620,height=370, relief= "solid",bd=2)
mainFrame.pack(side="bottom",pady=10)

Frame1 = tk.Frame(mainFrame,width=600,height = 100,relief="solid", bd=1)
Frame1.place(x=7,y=5)

ent_guess = tk.Entry(mainFrame,width=17,font = FONT)
ent_guess.place(x=15,y = 15)

Frame2 = tk.Frame(mainFrame,width=600,height = 250, relief="solid", bd=1)
Frame2.place(x=7,y=110)

# # 스크롤바 생성
scroll = tk.Scrollbar(Frame2)
scroll.pack(side = 'right', fill='y')
# # # 텍스트 리스트 생성
chat_box= tk.Listbox(Frame2,width=35,height=8,relief="solid",bd=2  ,yscrollcommand=scroll.set,font=LISTBOX_FONT)
chat_box.pack(side="left",fill="y")

scroll.configure(command=chat_box.yview)  #yview = 리스트의 y축 위치를 반환 =>scrollbar가 y의 위치를 반환

check = tk.Button(Frame2,text="0",width=10,height=10)
check.pack(side='right',fill='y')



answer = [1,3,5]
idx = 0
try_cnt = 10


def get_entry():
    global idx,try_cnt
    guess = ent_guess.get()
    if not guess:
        return
    try_cnt -= 1
    ball,strike= 0,0,
    guess = list(map(int,guess.split()))
    print(guess)

    if ent_guess == answer:
        ent_guess.insert(0,"게임종료")
        exit()
    for i in range(len(answer)):
        for j in range(len(guess)):
            if guess[j] == answer[i]:
                if i == j:
                    strike += 1
                else:
                    ball += 1
                break
    if ball == strike == 0:
        result = "FOUL"
    else:
        result = f"{strike}STRIKE {ball}BALL"
    chat_box.insert(idx,result)
    idx += 1
    ent_guess.delete(0,'end')


    print(guess)

check.configure(command=get_entry)


window.mainloop()
