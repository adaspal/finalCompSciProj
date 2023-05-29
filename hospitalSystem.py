import csv
from tkinter import *

def loginPage():
    for widget in frameMain.winfo_children():
        widget.destroy()
    frameLogin = Frame(frameMain)
    frameLogin.pack()
    loginLabel = Label(frameLogin, text="Login", font=('Helvetica', 36, "bold"))
    loginLabel.pack(pady=30)  # padding from the top

    # Create input fields for username and password
    labelUsername = Label(frameLogin, text="Username:")
    labelUsername.pack()
    entryUsername = Entry(frameLogin)
    entryUsername.pack()

    labelPassword = Label(frameLogin, text="Password:")
    labelPassword.pack()
    entryPassword = Entry(frameLogin, show="*")  # Mask password with asterisks
    entryPassword.pack()

    loginButton = Button(frameLogin, text="Sign in", command=lambda: loginValidation(entryUsername.get(), entryPassword.get()))
    loginButton.pack(pady=25)

    createAccountButton = Button(frameLogin, text="Don't Have an Account? Click Here", fg='blue', command=createAccountPage)
    createAccountButton.pack(pady=20)

    # errorLabel = Label(frameMain, font=("Helvetica", 16), fg="red")  # Create the error label to config under validation so that it only appears once

def createAccountPage():
    for widget in frameMain.winfo_children():
        widget.destroy()
    frameCreateAccount = Frame(frameMain)
    frameCreateAccount.pack(fill="both", expand=True)

    loginLabel = Label(frameCreateAccount, text="New Account", font=('Helvetica', 36, "bold"))
    loginLabel.pack(pady=30)  # padding from the top

    # Create input fields for username and password
    labelCreatedUsername = Label(frameCreateAccount, text="Username:")
    labelCreatedUsername.pack()
    entryCreatedUsername = Entry(frameCreateAccount)
    entryCreatedUsername.pack()

    labelCreatedPassword = Label(frameCreateAccount, text="Password:")
    labelCreatedPassword.pack()
    entryCreatedPassword = Entry(frameCreateAccount)
    entryCreatedPassword.pack()

    createAccountButton = Button(frameCreateAccount, text="Create Account", command=lambda: addNewAccount(entryCreatedUsername.get(), entryCreatedPassword.get()))
    createAccountButton.pack(pady=25)

    loginButton = Button(frameCreateAccount, text="Log in", command=loginPage)
    loginButton.pack()

    # createAccountButton = Button(frameCreateAccount, text="Don't Have an Account? Click Here", fg='blue', command=createAccount)
    # createAccountButton.pack(pady=20)

def validateNewAccount(createdUsername, createdPassword):
    #Checks to ensure that characters are used in the username and password
    if createdUsername.strip() == "" or createdPassword.strip() == "":
        return False

    #checks to see if an account with the same credentials already exists
    with open("doctorCredentials.csv", 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row[0] == createdUsername and row[1] == createdPassword:
                return False
            
    #If it passes both validations:
    return True

def addNewAccount(createdUsername, createdPassword):
    if validateNewAccount(createdUsername, createdPassword): #if the function returned true, meaning it passed validation
        #append to csv goes here
        errorLabel = Label(frameMain, text="✓ -Account created successfully! Please log in.", font=("Helvetica", 16), fg="green", bg="#C7F6B6")
        errorLabel.pack(pady=50)
    else:
        errorLabel = Label(frameMain, text="X -This account is invalid or already exists. Please try again.", font=("Helvetica", 16), fg="red", bg="#FFE2E1")
        errorLabel.pack(pady=50)

# Log in / create account functions go here ###
def validateCredentials(username, password):
    # Read credentials and validate
    with open("doctorCredentials.csv", 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row[0] == username and row[1] == password:
                return True
    return False

def loginValidation(username, password):
    if validateCredentials(username, password): #if the function returned true, meaning it passed validation
        for widget in frameMain.winfo_children():
            widget.destroy()
        homePage()
        #return username #find a way to assign a variable to the validated username in the main code, so that it can be passed through other functions
    else:
        print("Try again")
        errorLabel = Label(frameMain, text="X -Incorrect username and/or password. Please try again.", font=("Helvetica", 16), fg="red", bg="#FFE2E1")
        errorLabel.pack(pady=5)

def homePage():
    # Create home page
    frameHome = Frame(frameMain, bg="red")
    frameHome.pack(fill="both", expand=True)

    homeLabel = Label(frameHome, text=f"WELCOME", bg="red")
    homeLabel.pack()

    loginButton = Button(frameHome, text="Sign in", command=delete)
    loginButton.pack(pady=25)

def delete():
    for widget in frameMain.winfo_children():
        widget.destroy()
    frameDelete = Frame(frameMain, bg="green")
    frameDelete.pack(fill="both", expand=True)


# Main Code
win = Tk()
win.title("Hospital System")
win.geometry("700x500")

# Doesn't allow the screen to be resized
win.resizable(0, 0)

frameMain = Frame(win) #All other created frames are children of this frame, making them contained under frameMain
frameMain.pack(expand=True, anchor="n") 

loginPage()

win.mainloop()