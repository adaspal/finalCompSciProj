import csv
from csv import writer
from tkinter import *
from PIL import ImageTk, Image

def loginPage():
    '''Creates log in page'''
    for widget in frameMain.winfo_children():
        widget.destroy()
    frameLogin = Frame(frameMain)
    frameLogin.pack()

    # imageBg = Image.open("DocHospital-Bg.png")
    # # Create a PhotoImage object
    # photoBg = ImageTk.PhotoImage(imageBg)
    # labelBg = Label(frameLogin, image=photoBg)
    # labelBg.image = photoBg  # Keep a reference to the photo object
    # labelBg.pack()
    
    
    imageLogo = Image.open("DocCare-Logo.png")
    imageLogo = imageLogo.resize((300, 150)) # resizes (width, height)
    # Create a PhotoImage object
    photoLogo = ImageTk.PhotoImage(imageLogo)
    logolabel = Label(frameLogin, image=photoLogo)
    logolabel.image = photoLogo  # Keep a reference to the photo object
    logolabel.pack()

    # Page Header
    loginLabel = Label(frameLogin, text="Login", font=('Helvetica', 36, "bold"))
    loginLabel.pack(pady=10)  # padding from the top

    # Create input fields for username and password
    labelUsername = Label(frameLogin, text="Username:")
    labelUsername.pack()
    entryUsername = Entry(frameLogin)
    entryUsername.pack()

    labelPassword = Label(frameLogin, text="Password:")
    labelPassword.pack()
    entryPassword = Entry(frameLogin, show="*")  # Mask password with asterisks
    entryPassword.pack()
    
    loginButton = Button(frameLogin, text="Sign in", command=lambda: login(entryUsername.get(), entryPassword.get()))
    loginButton.pack(pady=25)

    createAccountButton = Button(frameLogin, text="Don't Have an Account? Click Here", fg='blue', command=createAccountPage)
    createAccountButton.pack(pady=15)

    # errorLabel = Label(frameMain, font=("Helvetica", 16), fg="red")  # Create the error label to config under validation so that it only appears once

def createAccountPage():
    ''' Creates create account page'''
    for widget in frameMain.winfo_children():
        widget.destroy()
    frameCreateAccount = Frame(frameMain)
    frameCreateAccount.pack(fill="both", expand=True)

    image = Image.open("DocCare-Logo.png")
    image = image.resize((300, 150)) # resizes (width, height)
    # Create a PhotoImage object
    photo = ImageTk.PhotoImage(image)
    logolabel = Label(frameCreateAccount, image=photo)
    logolabel.image = photo  # Keep a reference to the photo object
    logolabel.pack()

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

def homePage():
    ''' Creates home page'''
    # Create home page
    frameHome = Frame(frameMain, bg="red")
    frameHome.pack(fill="both", expand=True)

    homeLabel = Label(frameHome, text=f"WELCOME", bg="red")
    homeLabel.pack()

def validateNewAccount(createdUsername, createdPassword):
    ''' Validates that the account doesnt already exist'''
    #Checks to ensure that characters are used in the username and password
    if createdUsername.strip() == "" or createdPassword.strip() == "":
        return False

    #checks to see if an account with the same credentials already exists
    with open("doctorCredentials.csv", 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            print(row)
            if row[0] == createdUsername:
                return False
            
    #If it passes both validations:
    return True

def addNewAccount(createdUsername, createdPassword):
    '''Creates new account'''
    if validateNewAccount(createdUsername, createdPassword): #if the function returned true, meaning it passed validation
        #clearing screen
        for widget in frameMain.winfo_children():
            widget.destroy()
        newAccountList = [createdUsername, createdPassword]
        with open("doctorCredentials.csv", "a+", newline='') as file:
            csv_writer = writer(file)
            csv_writer.writerow(newAccountList)
                     
        homePage()
    else:
        errorLabel2 = Label(frameMain, text="X -This account is invalid or already exists. Please try again.", font=("Helvetica", 16), fg="red", bg="#FFE2E1")
        errorLabel2.pack(pady=20)
        print("error")

def validateCredentials(username, password):
    # Read credentials and validate
    with open("doctorCredentials.csv", 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row[0] == username and row[1] == password:
                return True
    return False

def login(username, password):
    '''Using validate credentials will allow you to log in or not'''
    if validateCredentials(username, password): #if the function returned true, meaning it passed validation
        for widget in frameMain.winfo_children():
            widget.destroy()
        homePage()
        #return username #find a way to assign a variable to the validated username in the main code, so that it can be passed through other functions
    else:
        print("Try again")
        errorLabel = Label(frameMain, text="X -Incorrect username and/or password. Please try again.", font=("Helvetica", 16), fg="red", bg="#FFE2E1")
        errorLabel.pack(pady=5)



# Main Code
win = Tk()
win.title("DocCare Hospital System")
win.geometry("700x500")

# Doesn't allow the screen to be resized
win.resizable(0, 0)

frameMain = Frame(win) #All other created frames are children of this frame, making them contained under frameMain
frameMain.pack(expand=True, anchor="n") 

loginPage()

win.mainloop()