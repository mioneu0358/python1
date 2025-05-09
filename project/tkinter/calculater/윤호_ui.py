import tkinter as tk
import tkinter.font as font
import tkinter.messagebox as msgbox

from solution import calculate

window = tk.Tk()
window.title("사칙연산계산기")
window.geometry("800x400+100+100")

entry_font = font.Font(size=40)
exp_entry = tk.Entry(window,relief='solid',font=entry_font)
exp_entry.place(x=20,y=10,width=560, height=100,)

btn_frame = tk.Frame(window, relief='solid',bd=1)
btn_frame.place(x=20, y=130, width=331, height=233)

nums_btn_geometries = [(i,j) for i in range(4) for j in range(3) ]
nums_btn_text = ['1','2','3','4','5','6','7','8','9','del','0','C']
btn_infos = list(zip(nums_btn_text, nums_btn_geometries))

def func_del():
    exp_entry.delete(len(exp_entry.get()) - 1)
    exp = exp_entry.get()
    if exp and exp[-1] == ' ':
        exp_entry.delete(len(exp) - 1)
def func_eq():
    exp = exp_entry.get()
    result = calculate(exp)
    if type(result) == str:
        msgbox.showerror("계산 오류", result)
    else:
        history_box.insert('end',f" {exp} = {result}\n")
        exp_entry.insert('end',f" = {result}")



for text, (x,y) in btn_infos:
    btn_font = font.Font(size=25)
    if text.isdigit():
        btn = tk.Button(btn_frame, text=text,width=5 ,font=btn_font,relief='raised',command=lambda t = text: exp_entry.insert('end',t))

    elif text == 'del':
        btn = tk.Button(btn_frame, text=text,width=5,font=btn_font,relief='raised', command=func_del)

    else:
        btn = tk.Button(btn_frame, text=text,width=5,font=btn_font,relief='raised',command = lambda : exp_entry.delete(0,'end') )
    btn.grid(row=x,column=y,rowspan=1,columnspan=1)

op_btn_geometries = [(i,0) for i in range(5)]
op_btn_text = ['+','-','x','÷']
op_btn_infos = list(zip(op_btn_text, op_btn_geometries))
print(op_btn_infos)

op_frame = tk.Frame(window, relief='solid', bd=1)
op_frame.place(x=360,y=130, width=222,height=233)

for text,(x,y) in op_btn_infos:
    btn = tk.Button(op_frame, text=text, width=5, font=btn_font,command=lambda t=text: exp_entry.insert('end', ' '+t+' '),relief='raised')
    btn.grid(row=x,column=y,sticky='wens')


btn_eq = tk.Button(op_frame, text='=', width=5, font=btn_font,command=func_eq )
btn_eq.grid(row=0,column=1,sticky='wens', rowspan=4)

history_box = tk.Text(window, font=("Consolas", 12), state='normal', relief='solid', bg="#f0f0f0")
history_box.place(x=590, y=10, width=200, height=355)

window.mainloop()
