from tkinter import *  
from tkinter import messagebox
  
def clicked():  
    # msg = messagebox.showerror('Ошибка доступа', 'В доступе отказано',)
    msg = messagebox.showinfo('Сообщение', 'Доступ Разрешён!',)
  
window = Tk()  
window.title("Password")  
window.geometry('400x200')  
lbl = Label(window, text="Введите пароль:")
lbl.configure(font=("Courier", 14))  
lbl.place(x=116, y=50)
txt = Entry(window,width=30)  
txt.place(x=110, y=100)  
btn = Button(window, text="Далее", command=clicked, width=10, height=2)  
btn.place(x=145, y=140)
btn.configure(font=("Courier", 12, "bold"))  
window.mainloop()