from tkinter import *

def loginPage():
    for widget in frameMain.winfo_children():
        widget.destroy()
    frameLogin = Frame(frameMain)
    frameLogin.pack()
    loginLabel = Label(frameLogin, text="Login", font=('Helvetica', 36, "bold"))
    loginLabel.pack(pady=30)
    
    labelUsername = Label(frameLogin, text="Username:")
    labelUsername.pack()
    entryUsername = Entry(frameLogin)
    entryUsername.pack()

    labelPassword = Label(frameLogin, text="Password:")
    labelPassword.pack()
    entryPassword = Entry(frameLogin, show="*")  # Mask password with asterisks
    entryPassword.pack()


win = Tk()
win.title("Hospital System")
win.geometry("700x500")

# Doesn't allow the screen to be resized
win.resizable(0, 0)

frameMain = Frame(win) #All other created frames are children of this frame, making them contained under frameMain
frameMain.pack(expand=True, anchor="n")

win.mainloop()