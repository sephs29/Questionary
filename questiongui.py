from tkinter import *
from PIL import ImageTk, Image
from questionary import get_data
from tkinter.messagebox import *


def mainscreen():
    global wd,ht,xpos,ypos,details, radiogroup  
    obj = get_data()
    details = obj.get_quesoptions("newipl2019.csv")
    #print(details)
    
    wd,ht,xpos,ypos = 1300, 650, 0, 0
    window1 = Tk()
    window1.title("Questionary")
    window1.geometry("{}x{}+{}+{}".format(wd,ht,xpos,ypos))
    window1.configure(bg="black")
    window1.grid_rowconfigure(0, weight=1)
    window1.grid_columnconfigure(0, weight=1)

    frame = Frame(window1, bg="black")
    frame.grid(row=0, column=0)  
    
    question = Label(
        frame, text=details[0], font=("Arial", 28, "bold"), bg="black", fg="gray80"
    )
    question.grid(row=0, column=0, columnspan=2, pady=(0, 30),sticky = N)
    
    radiogroup = IntVar()
    positionlist = {"R0": (1, 0), "R1": (1, 1), "R2": (2, 0), "R3": (2, 1)}
        
    for i, value in enumerate(positionlist):
        img = Image.open(details[1][i][2])
        img.thumbnail((250, 250), Image.NEAREST)
        img = ImageTk.PhotoImage(img)
        R = Radiobutton(
            frame,
            indicatoron=0,
            text=details[1][i][1],
            # selectimage = img,
            image=img,
            height=270,
            width=270,
            # padx = 100,
            command= lambda : popupscreen(window1),
            variable=radiogroup,
            value=details[1][i][0],
            bg="black",
            # activebackground = 'gray75',
        )

        R.grid(row=positionlist[value][0], column=positionlist[value][1])
        R.image = img
    radiogroup.set(-1)

    window1.mainloop()


def popupscreen(screen):
    screen.destroy()

    popup  = Tk()
    #window1.title("Message")
    popup.geometry("{}x{}+{}+{}".format(400,200,200,200))    
    popup.configure(bg="black", borderwidth = 2, )
    popup.grid_rowconfigure(0, weight=1)
    popup.grid_columnconfigure(0, weight=1)
    
    #popup.overrideredirect(True) # turns off title bar, geometry
    title_bar = Frame(popup, bg = "black", relief="flat", bd=2,)
    title_bar.grid(row= 0,column =0, sticky =N+E+W)
    title = Label(title_bar, text="Message", bg="black", fg="gray85",font = ("Arial", 15, "bold"),)
    title.grid(row=0, column=0)
    close_button = Button(popup, text="X", bg="grey65", command=popup.destroy)
    close_button.grid(row = 0,column = 2, sticky= N+E)
        
    answer  = AnswerCheck()
    
    popupbody = Label(popup,text = answer ,font =('Arial', 15, 'bold'),bg = 'black', fg = 'red')
    popupbody.grid(row = 0, column = 0)
    okay_button = Button(popup, text="OKAY", bg="grey65", width = 8, height = 2, command= lambda:call_mainscreen(popup))    
    okay_button.grid(row = 0,column = 0, sticky= S,padx = (0,10))
    
    popup.mainloop()
    
def AnswerCheck():
    selected = radiogroup.get()
    if selected == details[2][0]:
        answer = 'Correct Answer !'
    else:
        answer = 'Wrong Answer !'
    
    return answer       
    
def call_mainscreen(window):
    window.destroy()
    mainscreen()
    




if __name__ == "__main__":
    #popupscreen()
    mainscreen()
