import csv

### Log in / create account functions go here ###
def validateCredentials(username, password):
 # reads credentials validates 
    with open("doctorCredentials.csv", 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row[0] == username:
                return True
        return False


### View patient functions go here ###

### Add patient functions go here ###

### ML stuff ###

### Change patient information ###

#GUI stuff

def homePage():
    # creates home page
    frame2 = Frame(frameLogin, bg="red")
    frame2.pack(fill="both", expand=1) 
from tkinter import *
win = Tk()
win.title("Hospital System")
win.geometry("700x500")

# Doesn't allow the screen to be resized
win.resizable(0, 0)

frameLogin = Frame(win)
frameLogin.pack(side="top", expand=True, fill="both")

loginLabel = Label(frameLogin, text="Login", font=('Helvetica', 36, "bold"))
loginLabel.pack(pady=30)  # padding from the top

def login():
    username = entryUsername.get()
    password = entryPassword.get()
    if validateCredentials(username, password) == True:
        for widget in frameLogin.winfo_children():
            widget.destroy()
        homePage()
    else:
        print("try again")

        ## display error message ask to retry
        

# Create input fields for first name, last name, and password
labelUsername = Label(frameLogin, text="Username:")
labelUsername.pack() #can run again
entryUsername = Entry(frameLogin)
entryUsername.pack()

labelPassword = Label(frameLogin, text="Password:")
labelPassword.pack()
entryPassword = Entry(frameLogin, show="*")  # Mask password with asterisks
entryPassword.pack()

loginButton = Button(frameLogin, text="Sign in", command=login)
loginButton.pack(pady=25)




# def create_red_frame():
#     # Destroy previous widgets in frameLogin
#     for widget in frameLogin.winfo_children():
#         widget.destroy()

#     # Create a black frame with red background
#     frame2 = Frame(frameLogin, bg="red")
#     frame2.pack(fill="both", expand=1)


# def quit_program():
#     win.destroy()


# # Create two buttons
# b1 = Button(frameLogin, command=create_red_frame, text="Continue")
# b1.pack(pady=10)

# b2 = Button(frameLogin, command=quit_program, text="Quit")
# b2.pack(pady=10)

win.mainloop()






