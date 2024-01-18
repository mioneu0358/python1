import tkinter as tk
import tkinter.font
import tkinter.messagebox as msBox
import random


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
guess_list = tk.Listbox(Frame2,width=35,height=8,relief="solid",bd=2  ,yscrollcommand=scroll.set,font=LISTBOX_FONT)
guess_list.pack(side="left",fill="y")

scroll.configure(command=guess_list.yview)  #yview = 리스트의 y축 위치를 반환 =>scrollbar가 y의 위치를 반환

check = tk.Button(Frame2,text="Enter",width=10,height=10,)
check.pack(side='right',fill='y')




answer = []
idx = 0
try_cnt = 10

def init_answer():
    answer.clear()
    while len(answer) < 3:
        x = random.randint(0, 9)
        if x not in answer:
            answer.append(x)
def restart():
    global idx,try_cnt
    init_answer()
    ent_guess.delete(0,'end')
    guess_list.delete(0,idx)
    idx,try_cnt = 0,10


def get_entry(event):
    print(event)
    global idx,try_cnt
    guess = ent_guess.get()
    if not guess:
        return
    try_cnt -= 1
    ball,strike= 0,0,
    guess = list(map(int,guess.split()))

    for i in range(len(answer)):
        for j in range(len(guess)):
            if guess[j] == answer[i]:
                if i == j:
                    strike += 1
                else:
                    ball += 1
                break
    if strike == 3:
        ent_guess.insert(0,"정답입니다 ")
        result = msBox.askokcancel(f"축하합니다. 시도횟수: {10 - try_cnt}", "다시 시작하시겠습니까?")
        if result:
            restart()
            return
        else:
            exit()

    if ball == strike == 0:
        result = f"[{10-try_cnt}] {guess}:FOUL"
    else:
        result = f"[{10-try_cnt}] {guess}: {strike}STRIKE {ball}BALL"
    guess_list.insert(idx,result)
    idx += 1
    ent_guess.delete(0,'end')

check.bind("<Button 1>", get_entry)
ent_guess.bind("<Return>",get_entry)

init_answer()
print(answer)
window.mainloop()
