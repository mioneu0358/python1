import tkinter as tk
import tkinter.font as font
import main
window = tk.Tk()
window.title("사칙연산계산기")
window.geometry("600x400+100+100")

entry_font = font.Font(size=40)
exp_entry = tk.Entry(window,relief='solid',font=entry_font)
exp_entry.place(x=20,y=10,width=560, height=100,)

btn_frame = tk.Frame(window, relief='solid',bd=1)
btn_frame.place(x=20, y=130, width=331, height=233)

nums_btn_geometries = [(i,j) for i in range(4) for j in range(3) ]
nums_btn_text = ['1','2','3','4','5','6','7','8','9','del','0','C']
btn_infos = list(zip(nums_btn_text, nums_btn_geometries))
print(btn_infos)
def insert_num():
    exp_entry.insert('end', text)

for text, (x,y) in btn_infos:
    btn_font = font.Font(size=25)
    if text.isdigit():
        btn = tk.Button(btn_frame, text=text,width=5 ,state="normal",command=lambda t = text: exp_entry.insert('end',t),font=btn_font)

    elif text == 'del':
        btn = tk.Button(btn_frame, text=text,width=5,font=btn_font, command=lambda : exp_entry.delete(-1,-1))

    else:
        btn = tk.Button(btn_frame, text=text,width=5,font=btn_font,command = lambda : exp_entry.delete(0,'end') )
    btn.grid(row=x,column=y,rowspan=1,columnspan=1)

op_btn_geometries = [(0,i) for i in range(5)]
op_btn_text = ['+','-','x','÷']
op_btn_infos = list(zip(op_btn_text, op_btn_geometries))

window.mainloop()

