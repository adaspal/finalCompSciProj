# File imports
import csv
from csv import writer

# Tkinter imports
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

# General ML imports
import os
import gzip
import numpy as np
import matplotlib.pyplot as plt #For graphing
from pylab import cm
import warnings

# Dataset imports for ML
import pandas as pd
import opendatasets as od
import numpy as np

warnings.filterwarnings("ignore")

# scikit-learn imports for ML
from sklearn import datasets
from sklearn.model_selection import train_test_split   
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA           
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# Neural Networks import
from sklearn.neural_network import MLPClassifier

def clearPage():
    '''
    Function clears all the widgets displayed in the main frame
    '''
    for widget in frameMain.winfo_children():
        widget.destroy()

def loginPage():
    '''
    Creates login page that is called as the first function in the code.
    Prompts the user for their username and password, which are passed on for validation 
    The page displays a button option to create an account
    '''
    clearPage()
    frameLogin = Frame(frameMain)
    frameLogin.pack()

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

    createAccountButton = Button(frameLogin, text="Don't Have an Account? Click Here", fg='#127ca1', command=createAccountPage) #background is a turquoise hexcode
    createAccountButton.pack()


def createAccountPage():
    ''' 
    Creates a page that takes in a unique username and password to make a new account 
    Calls the addNewAccount function, which will validate the account and add it to the database
    '''
    clearPage()
    frameCreateAccount = Frame(frameMain)
    frameCreateAccount.pack(fill="both", expand=True)

    imageLogo = Image.open("DocCare-Logo.png")
    imageLogo = imageLogo.resize((300, 150)) # resizes (width, height)
    # Create a PhotoImage object
    photoLogo = ImageTk.PhotoImage(imageLogo)
    logolabel = Label(frameCreateAccount, image=photoLogo)
    logolabel.image = photoLogo  # Keep a reference to the photo object
    logolabel.pack()

    loginLabel = Label(frameCreateAccount, text="New Account", font=('Helvetica', 36, "bold"))
    loginLabel.pack(pady=20)  # padding from the top

    # Create input fields for username and password
    labelCreatedUsername = Label(frameCreateAccount, text="Username:")
    labelCreatedUsername.pack()
    entryCreatedUsername = Entry(frameCreateAccount)
    entryCreatedUsername.pack()

    labelCreatedPassword = Label(frameCreateAccount, text="Password:")
    labelCreatedPassword.pack()
    entryCreatedPassword = Entry(frameCreateAccount, show="*")
    entryCreatedPassword.pack()

    createAccountButton = Button(frameCreateAccount, text="Create Account", command=lambda: addNewAccount(entryCreatedUsername.get(), entryCreatedPassword.get()))
    createAccountButton.pack(pady=20)

    createBackButton = Button(frameCreateAccount, text="← Back", command=lambda: loginPage())
    createBackButton.pack()

def homePage(usr):
    ''' 
    Creates a homepage which welcomes the user by using the usr parameter and displays all of the menu options
    ''' 

    clearPage()
    # Create home page
    frameHome = Frame(frameMain)
    frameHome.pack(fill="both", expand=True)

    #Main header which welcomes user
    homeLabel = Label(frameHome, text=f"Welcome, " + usr, font=('Helvetica', 36, "bold"))
    homeLabel.pack(pady=10)

    #Menu options as buttons
    viewButton = Button(frameHome, text="View Patient", fg='#127ca1', command=lambda: viewPatientPage(usr))
    viewButton.pack(pady=20)
    addButton = Button(frameHome, text="Add Patient", fg='#127ca1', command=lambda: addPatientPage(usr))
    addButton.pack(pady=20)
    changeButton = Button(frameHome, text="Change Patient", fg='#127ca1', command=lambda: changePatientPage(usr))
    changeButton.pack(pady=20)
    graphButton = Button(frameHome, text="Graph Data", fg='#127ca1', command=lambda: graphCall(usr))
    graphButton.pack(pady=20)
    signOutButton = Button(frameHome, text="Sign Out", fg='#127ca1', command=lambda: signOut())
    signOutButton.pack(pady=20)
    
def signOut():
    '''
    Function runs as a command when sign out button is clicked.
    Used to bring the user back to the login page.
    '''
    #creating this function to run the login page makes the program more modular and easy to maintain
    loginPage()

def validateNewAccount(createdUsername, createdPassword):
    ''' 
    Validates that the account uses characters and doesn't already exist by checking if the inputted username and password 
    are stored in the same row in the doctor credentials database
    Returns True if username and password are unique and contain characters
    Returns False if username and password and both already used together or no characters are used
    '''
    #Checks to ensure that characters are used in the username and password
    if createdUsername.strip() == "" or createdPassword.strip() == "":
        return False

    #checks to see if an account with the same credentials already exists
    with open("doctorCredentials.csv", 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row[0] == createdUsername:
                return False
            
    #If it passes both validations:
    return True

def addNewAccount(createdUsername, createdPassword):
    '''
    Creates a new doctor account by storing the inputted username and password in the doctor credentials csv database
    If the username and password does not pass validation, an error message is displayed
    '''

    if validateNewAccount(createdUsername, createdPassword): #if the function returned true, meaning it passed validation
        newAccountList = [createdUsername, createdPassword]
        with open("doctorCredentials.csv", "a+", newline='') as file:
            csv_writer = writer(file) #adds new user to the doctor database
            csv_writer.writerow(newAccountList)
        usr = createdUsername             
        homePage(usr) #
    #if the account does not meet expectations
    else:
        if not hasattr(validateNewAccount, 'errorLabel2'):  # Check if errorLabel attribute exists so it does not create a new frame
            validateNewAccount.errorLabel2 = Label(frameMain)
            validateNewAccount.errorLabel2.pack(pady=10)
        validateNewAccount.errorLabel2.config(text="X -This account is invalid or already exists. Please try again.", font=("Helvetica", 16), fg="red", bg="#FFE2E1")
        

def validateCredentials(username, password):
    '''
    Reads the doctor credentials csv file to determine if a row has the same username and password as the inputs
    If the username and password inputed match a row, validation passed, account exists and function returns True 
    If the username and password inputed do not match a row, validation failed, account does not exist and function returns False
    '''
    # Reads credentials and validates if username and password already exist in the same row
    with open("doctorCredentials.csv", 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row[0] == username and row[1] == password:
                return True
    return False

def login(username, password):
    '''
    Directs the user to the homepage if their credentials were validated or displays an error message and stays on screen 
    if username and/or password does not oass validation. 
    '''
    if validateCredentials(username, password):
        usr = username
        homePage(usr) #goes to homepage and take the username as a parameter if validate credentials function returns true
    else:
        if not hasattr(login, 'errorLabel'):  # Checks if errorLabel attribute exists so it does not create a new frame
            login.errorLabel = Label(frameMain, font=("Helvetica", 16), fg="red", bg="#FFE2E1")
            login.errorLabel.pack(pady=15)
        login.errorLabel.config(text="X -Incorrect username and/or password. Please try again.")

def collectPatients(usr):
    '''
    The patient database csv file is read to find every patient under the logged in user, which is appended to a list
    Returns patients; list of user's patients
    '''
    patients = []
    with open("patientDatabase.csv", 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row[0] == usr:
                # appends user information without doctor name
                patients.append(row[1:])
    return patients

def viewPatientPage(usr):
    '''
    Creates a frame with a treeview that displays a horizontal table of the user's (usr) patients. 
    If the user has no patients to view, the screen prompts them to add a patient. 
    Returns: None
    '''

    #clears screen and creates a new frame
    clearPage()
    frameviewPatientPage = Frame(frameMain)
    frameviewPatientPage.pack(fill="both", expand=True)

    # collects all of the user's patients as a list
    patientsList = collectPatients(usr)

    if not patientsList:
        errorLabel = Label(frameviewPatientPage, text="You have no patients to view")
        errorLabel.pack()
        addButton = Button(frameviewPatientPage, text="Add Patient", fg='#127ca1', command=lambda: addPatientPage(usr))
        addButton.pack()
    else:
        tree = ttk.Treeview(frameviewPatientPage, xscrollcommand=True)

        # Define the columns for the table
        columns = ['Name', 'Age', 'Sex (F=0,M=1)', 'CP', 'TrestBPS', 'Chol', 'FBS', 'RestECG', 'Thalach', 'Exang', 'OldPeak', 'Slope', 'CA', 'Thal', 'Diagnoses']

        # Configure the Treeview columns
        tree["columns"] = columns
        tree.heading("#0", text="Index")
        tree.column("#0", width=50)

        # Configure each column
        column_width = 80  # Adjust this value as desired
        for column in columns:
            tree.heading(column, text=column)
            tree.column(column, width=column_width)

        # Insert data into the Treeview
        for index, patient in enumerate(patientsList):
            tree.insert('', 'end', text=index, values=patient)

        # Configure the scrollbar for horizontal scrolling
        scrollbar = ttk.Scrollbar(frameviewPatientPage, orient="horizontal", command=tree.xview)
        tree.configure(xscrollcommand=scrollbar.set)
        scrollbar.pack(side="bottom", fill="x")

        # Pack and display the Treeview
        tree.pack()

    createBackButton = Button(frameMain, text="← Back", command=lambda: homePage(usr))
    createBackButton.pack(pady=30)

def addPatientPage(usr):
    '''
    Takes inputs of patient information through different widgets. Passes selected information to next page.
    '''
    clearPage()
    frameaddPatientPage = Frame(frameMain)
    frameaddPatientPage.pack(fill="both", expand=True)
    addPLabel = Label(frameaddPatientPage, text="Add Your patient", font=('Helvetica', 36, "bold"))
    addPLabel.pack()
    # Patient name
    patientNameLabel = Label(frameaddPatientPage, text="Patient Name:")
    patientNameLabel.pack()
    entryPatient = Entry(frameaddPatientPage)
    entryPatient.pack()
    # Patient age
    ageLabel = Label(frameaddPatientPage, text="Age(0-130):")
    ageLabel.pack()
    ageSP = Spinbox(frameaddPatientPage, from_=0, to=100)
    ageSP.pack()
    # Gender
    sexSel = StringVar(frameaddPatientPage)
    sexSel.set("Sex: ")
    sexMenu = OptionMenu(frameaddPatientPage, sexSel, "Male","Female" )
    sexMenu.pack()
    # Chest pain type
    cptLabel = Label(frameaddPatientPage, text="Chest Pain Type:")
    cptLabel.pack()
    cptSel = StringVar(frameaddPatientPage)
    cptOptionZero = Radiobutton(frameaddPatientPage, text="0-Typical Angina", variable=cptSel, value= 0)
    cptOptionZero.pack()
    cptOptionOne = Radiobutton(frameaddPatientPage, text="1-Atypical Angina", variable=cptSel, value= 1)
    cptOptionOne.pack()
    cptOptionTwo = Radiobutton(frameaddPatientPage, text="2-Non-Anginal", variable=cptSel, value= 2)
    cptOptionTwo.pack()
    cptOptionThree = Radiobutton(frameaddPatientPage, text="3-Asymptomatic", variable=cptSel, value= 3)
    cptOptionThree.pack()
    # resting blood pressure
    bpsLabel = Label(frameaddPatientPage, text="Resting Blood Pressure(40-200):")
    bpsLabel.pack()
    bpsSP = Spinbox(frameaddPatientPage, from_=0, to=100)
    bpsSP.pack()
    # creates error label to be configured if inputs are invalid
    addPatientErrorLabel = Label(frameaddPatientPage)
    addPatientErrorLabel.pack()
    # once button is pressed, information is passed to next function to be validated
    nextButton = Button(frameaddPatientPage, text="Next", fg='#127ca1', command=lambda: addPatientPageTwo(addPatientErrorLabel, usr, entryPatient.get(),ageSP.get(), sexSel.get(), cptSel.get(), bpsSP.get() ))
    nextButton.pack()
    # goes home
    createBackButton = Button(frameaddPatientPage, text="← Back", command=lambda: homePage(usr))
    createBackButton.pack()


def addPatientPageTwo(label, doctor, patient, age, sex, cpt, rbp):
    '''
    Validates and creats list of previous inputs and displays new set of inputs
    '''
    # converts male and female inputs to integers
    if sex == "Male":
        sex = 1
    else: 
        sex = 0
    # creates health list with first set of data, this list will be added to as more inputs are given
    patientHealthList= [doctor, patient, age, sex, cpt, rbp]
    if validatePatientData(patientHealthList) == True:
        # if the health list is validate it will go to the next page to display next set of inputs
        clearPage()
        frameaddPatientPageTwo = Frame(frameMain)
        frameaddPatientPageTwo.pack(fill="both", expand=True)
        # cholesterol
        cholLabel = Label(frameaddPatientPageTwo, text="Cholesterol Level(0-300):")
        cholLabel.pack()
        cholSP = Spinbox(frameaddPatientPageTwo, from_=0, to=300)
        cholSP.pack()
        # fasting blood sugar
        fbpsSel = StringVar(frameaddPatientPageTwo)
        fbpsPatient = Label(frameaddPatientPageTwo, text="Fasting Blood Sugar:")
        fbpsPatient.pack()
        fbsOptionZero = Radiobutton(frameaddPatientPageTwo, text="0", variable=fbpsSel, value= 0)
        fbsOptionZero.pack()
        fbsOptionOne = Radiobutton(frameaddPatientPageTwo, text="1", variable=fbpsSel, value= 1)
        fbsOptionOne.pack()
        # resting ECG
        restecgSel = StringVar(frameaddPatientPageTwo)
        restecgPatient = Label(frameaddPatientPageTwo, text="Resting ECG Result:")
        restecgPatient.pack()
        restecgOptionZero = Radiobutton(frameaddPatientPageTwo, text="0", variable=restecgSel, value= 0)
        restecgOptionZero.pack()
        restecgOptionOne = Radiobutton(frameaddPatientPageTwo, text="1", variable=restecgSel, value= 1)
        restecgOptionOne.pack()
        restecgOptionTwo = Radiobutton(frameaddPatientPageTwo, text="2", variable=restecgSel, value= 2)
        restecgOptionTwo.pack()
        # max heart rate
        thalLabel = Label(frameaddPatientPageTwo, text="Max. Heart Rate Achieved(40-250):")
        thalLabel.pack()
        thalSP = Spinbox(frameaddPatientPageTwo, from_=40, to=250)
        thalSP.pack()
        # excersize induced angia
        exangSel = StringVar(frameaddPatientPageTwo)
        exangLabel = Label(frameaddPatientPageTwo, text="Excercise induced angia:")
        exangLabel.pack()
        exangOptionOne = Radiobutton(frameaddPatientPageTwo, text="Yes", variable=exangSel, value= 1)
        exangOptionOne.pack()
        exangOptionZero = Radiobutton(frameaddPatientPageTwo, text="No", variable=exangSel, value= 0)
        exangOptionZero.pack()
        # error label to be configured if inputs are invalid
        addPatientErrorLabel = Label(frameaddPatientPageTwo)
        addPatientErrorLabel.pack()
        # takes to next page to be validated
        nextButton = Button(frameaddPatientPageTwo, text="Next", fg='#127ca1', command=lambda: addPatientPageThree(addPatientErrorLabel, patientHealthList,cholSP.get(), fbpsSel.get(), restecgSel.get(), thalSP.get(), exangSel.get() ))
        nextButton.pack()

        createBackButton = Button(frameaddPatientPageTwo, text="← Back", command=lambda: addPatientPage(doctor))
        createBackButton.pack()
    else:
        # if invalid, label will display message
        label.config(text="Invalid / missing inputs.",font=("Helvetica", 16), fg="red", bg="#FFE2E1" )

        

def addPatientPageThree(label, patientHealthList, chol,fbs,restecg,thalach,exang):
    '''
    Adds and validates new inputs and displays final set of inputs
    '''
    # adds new inputs to list
    patientHealthList.extend([chol,fbs,restecg,thalach,exang])
    if validatePatientData(patientHealthList) == True:
        # if new inputs are valid, page is cleared to display final set of inputs 
        clearPage()
        frameaddPatientPageThree = Frame(frameMain)
        frameaddPatientPageThree.pack(fill="both", expand=True)
        # old peak
        oldpeakPatient = Label(frameaddPatientPageThree, text="St depression induced by excercise relative to rest(0-7):")
        oldpeakPatient.pack()
        oldpeakSP = Spinbox(frameaddPatientPageThree, from_=0, to=6,increment= 0.1)
        oldpeakSP.pack()
        #Slope
        slopeSel = StringVar(frameaddPatientPageThree)
        slopePatient = Label(frameaddPatientPageThree, text="Slope:")
        slopePatient.pack()
        slopeOptionZero = Radiobutton(frameaddPatientPageThree, text="0", variable=slopeSel, value= 0)
        slopeOptionZero.pack()
        slopeOptionOne = Radiobutton(frameaddPatientPageThree, text="1", variable=slopeSel, value= 1)
        slopeOptionOne.pack()
        slopeOptionTwo = Radiobutton(frameaddPatientPageThree, text="2", variable=slopeSel, value= 2)
        slopeOptionTwo.pack()
        # vessles coloured by floroscopy
        caSel = StringVar(frameaddPatientPageThree)
        caPatient = Label(frameaddPatientPageThree, text="Num of vessels coloured by floroscopy:")
        caPatient.pack()
        caOptionZero = Radiobutton(frameaddPatientPageThree, text="0", variable=caSel, value= 0)
        caOptionZero.pack()
        caOptionOne = Radiobutton(frameaddPatientPageThree, text="1", variable=caSel, value= 1)
        caOptionOne.pack()
        caOptionTwo = Radiobutton(frameaddPatientPageThree, text="2", variable=caSel, value= 2)
        caOptionTwo.pack()
        caOptionThree = Radiobutton(frameaddPatientPageThree, text="3", variable=caSel, value= 3)
        caOptionThree.pack()
        # Thal
        thalSel = StringVar(frameaddPatientPageThree)
        thalPatient = Label(frameaddPatientPageThree, text="thal:")
        thalPatient.pack()
        thalOptionOne = Radiobutton(frameaddPatientPageThree, text="normal", variable=thalSel, value= 1)
        thalOptionOne.pack()
        thalOptionTwo = Radiobutton(frameaddPatientPageThree, text="fixed defect", variable=thalSel, value= 2)
        thalOptionTwo.pack()
        thalOptionThree = Radiobutton(frameaddPatientPageThree, text="reversable defect", variable=thalSel, value= 3)
        thalOptionThree.pack()
        # error label to be configured if inputs are invalid
        addPatientErrorLabel = Label(frameaddPatientPageThree)
        addPatientErrorLabel.pack()
        # passes information to next page to be validated
        saveButton = Button(frameaddPatientPageThree, text="Save", fg='#127ca1', command=lambda: diagnosePatient(addPatientErrorLabel,patientHealthList,oldpeakSP.get(), slopeSel.get(), caSel.get(), thalSel.get() ))
        saveButton.pack()

        createBackButton = Button(frameaddPatientPageThree, text="← Back", command=lambda: addPatientPageTwo(label, patientHealthList[0],  patientHealthList[1], patientHealthList[2], patientHealthList[3],  patientHealthList[4],  patientHealthList[5]))
        createBackButton.pack()
    else:
        # removes new inputs added so that user can reenter
        patientHealthList.pop()
        patientHealthList.pop()
        patientHealthList.pop()
        patientHealthList.pop()
        patientHealthList.pop()
        # Configues label to display invalid message
        label.config(text="Invalid / missing inputs.",font=("Helvetica", 16), fg="red", bg="#FFE2E1" )
      
def validatePatientData(patientInfoList):
    '''
    Returns a boolean that checks if the list features are valid and inside the boundaries
    '''
    # Iterate through list starting from index 2 to skip doctor and patient name
    for index, item in enumerate(patientInfoList[2:]):
        # Checks if the item in list is a string
        if isinstance(item, str):
            # If the item is a string, then checks if the item consists of digits 
            # or is a float (to confirm input is valid)
            if item.isdigit() == True or isfloat(item) == True:
                # Through following if statements, checks which feature the list item is
                # Item is then converted from string to int to then be compared to boundaries
                # At any point if a list item is not valid, the function returns False
                if index == 0: #age feature
                    # Checks if age is a valid number
                    if 0 <= int(item) <= 130:
                        continue
                    else:
                        return False
                if index == 3: #resting blood pressure feature
                    # Checks if resting blood pressure is a valid number
                    if 40 <= int(item) <= 200:
                        continue
                    else:
                        return False
                if index == 4: #cholesterol feature
                    # Checks if cholesterol is a valid number
                    if 0 <= int(item) <= 300:
                        continue
                    else:
                        return False
                if index == 7: # Max. Heart Rate achieved feature
                    # Checks if max. heart rate achieved is a valid number
                    if 40 <= int(item) <= 250:
                        continue
                    else:
                        return False
                if index == 9: #oldpeak feature
                    # Checks if oldpeak feature is a valid number (this is a decimal so float)
                    if 0 <= float(item) <= 7:
                        continue
                    else:
                        return False
            else:
                return False
        # If the item is an int, then it must be an radio button thus it is valid for sure
        else:
            continue
    # If all list items are valid, function returns True    
    return True

def isfloat(num):
    '''
    Returns boolean that checks whether or not passed string can be converted to a float
    '''
    try:
        # Attempts to convert to float, if possible then returns True
        float(num)
        return True
    except ValueError:
        # If not possible to turn into float (throws exception), return False
        return False

def diagnosePatient(label,patientHealthList, oldpeak, slope, ca, thal):
    '''
    adds and validates final set of inputs. If valid, adds to patient database. If invalid, displays error for reentry
    '''
    patientHealthList.extend([oldpeak, slope, ca, thal])
    
    if validatePatientData(patientHealthList) == True:
        # Runs diagnoses on validated data and appends to end of list
        patientHealthList.append(neuralNetworks(patientHealthList))
        # Adds list to patient database
        addPatient(patientHealthList)
        # Displays sucess labek
        sucessfulAdditionPage(patientHealthList[0])     
    else:
        # removes invalid inputs so that user can reenter
        patientHealthList.pop()
        patientHealthList.pop()
        patientHealthList.pop()
        patientHealthList.pop()        
        # displays error message
        label.config(text="Invalid / missing inputs.",font=("Helvetica", 16), fg="red", bg="#FFE2E1" )

def sucessfulAdditionPage(usr):
        '''
        Displays label and options to go home, view patients or add another patient
        '''
        clearPage()
        framepatientDiagnosed = Frame(frameMain)
        framepatientDiagnosed.pack(fill="both", expand=True)  
        # sucess label      
        successLabel = Label(framepatientDiagnosed)
        successLabel.config(text="✓ -Patient added successfully!", font=("Helvetica", 16), fg="green", bg="#C7F6B6")
        successLabel.pack(pady=10)
        # view button
        viewButton = Button(framepatientDiagnosed, text="View All Patients", fg='#127ca1', command=lambda: viewPatientPage(usr))
        viewButton.pack(pady=5)
        # add another patient
        addButton = Button(framepatientDiagnosed, text="Add Another Patient", fg='#127ca1', command=lambda: addPatientPage(usr))
        addButton.pack(pady=5) 
        # home button       
        createBackButton = Button(framepatientDiagnosed, text="← Back", command=lambda: homePage(usr))
        createBackButton.pack()  

def addPatient(list):
    '''Takes the list passed and appends to patient database file'''
    with open("patientDatabase.csv", 'a', newline="") as file:
       csv_writer = writer(file)
       csv_writer.writerow(list)


def neuralNetworks(list): 
    '''
    This function takes the patient list as parameter and runs the neural network (NN) on the data.
    NN is a type of ML process, called deep learning, that uses interconnected nodes in a layered 
    structure that resembles the human brain. Here we call the MLP classifier from scikit learn and
    use NN as a black box.
    Function returns a string prediction either "Positive" or "Negative"
    '''
    # Get data from csv file and read using pandas
    data = pd.read_csv('heart.csv')

    # y is the target (diagnosis given in the dataset)
    y=data.target
    # x are all the remaining features aside from the target (thus "drop" the target)
    x=data.drop('target',axis=1)

    # Test size is set to 0.4 so 40% of the total dataset is used to test the model and 60%
    # is used to train the NN model
    sample_train, sample_val, labels_train, labels_val = train_test_split(x,y,test_size=0.4, random_state=42)

    # Use numpy to set variables to numpy
    sample_train = sample_train.to_numpy()
    sample_val = sample_val.to_numpy()

    # Standardize
    ss = StandardScaler()
    sample_train = ss.fit_transform(sample_train)
    sample_val = ss.transform(sample_val)

    # Set the dimension to 13; dimension rep. the # of fwatures that will be used to find the model
    # We set it to the max. number (13 features) to maximize accuracy
    N_DIM = 13
    # PCA is principal component analysis: sets dimension of the dataset and summarizes the data for NN
    pca = PCA(n_components=N_DIM)
    sample_train = pca.fit_transform(sample_train)
    sample_val = pca.transform(sample_val)
    
    # Initializes the neural network that will be run
    nn = MLPClassifier()
    # Data fed into NN model and model is trained and tested (ready to be used for prediction)
    nn.fit(sample_train, labels_train)
    # NN score calculated 
    nnScore = nn.score(sample_val, labels_val) * 100
    nnScore = round(nnScore, 2)
    # prints NN score of model based on testing in the terminal
    print(f"NN test score: {nnScore}" + "%")

    # all the fwatures of the list are converted to ints and saved into variables named the feature
    age = int(list[2])      # Starts from index 2 to skip doctor and patient names in list
    sex = int(list[3])
    cp = int(list[4])
    trestbps = int(list[5])
    chol = int(list[6])
    fbs = int(list[7])
    restecg = int(list[8])
    thalach = int(list[9])
    exang = int(list[10])
    oldpeak = float(list[11])
    slope = int(list[12])
    ca = int(list[13])
    thal = int(list[14])
    # Creates numpy array with all the int variables
    features = np.array([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])
    # Saves NN prediction calculated through features array into prediction variable
    prediction = nn.predict(features)
    prediction = prediction[0]
    # Checks if prediction is negative (0) or positive (1) and saves diagnosis to predicton
    if prediction == 0:
        prediction = 'Negative'
    else:
        prediction = 'Positive'
    # returns string prediction diagnosis
    return prediction

def changePatientPage(usr):
    '''
    Passes doctor as paramameter
    Displays list of patients that doctors can select from to edit their information
    '''
    # clears previous page and creates page
    clearPage()
    framechangePatient = Frame(frameMain)
    framechangePatient.pack(fill="both", expand=True)

    # creates list of patients that doctors can select
    patientNameList = []
    for item in collectPatients(usr):
        patientNameList.append(item[0])
    # if list is empty, doctor cannot change any patients
    if not patientNameList:
        errorLabel = Label(framechangePatient, text="You have no patients to change.")
        errorLabel.pack()
        addButton = Button(framechangePatient, text="Add patient", fg='#127ca1', command=lambda: addPatientPage(usr))
        addButton.pack(side='left')
        createBackButton = Button(framechangePatient,text="← Back", command=lambda: homePage(usr))
        createBackButton.pack(side='right')
    else: # if doctor has patients
        # option menu for patients to select from
        patientSel = StringVar(framechangePatient)
        patientSel.set("Patient: ")
        # when selected, dircts to display page
        patientMenu = OptionMenu(framechangePatient, patientSel,*patientNameList, command= lambda x: displayChart(usr, patientSel.get()))
        patientMenu.pack()
        # back button to go back home
        createBackButton = Button(frameMain, text="← Back", command=lambda: homePage(usr))
        createBackButton.pack(pady=30)


def infoListGen(doctor, patient):
    '''
    Generates a list of one patients infomation
    Passes doctor and desired patient
    Returns patients data
    '''
    # creates a list of all patients datas from that doctor
    for item in collectPatients(doctor):
        # traverse through list to identify desired patient data
        if item[0] == patient:
            # save only that data to a new list
            infoList = item
    return infoList
    

def displayChart(doctor, patient):
    '''
    Displays patients data in a chart to select from to change factors
    '''
    clearPage()
    framedisplayChart = Frame(frameMain)
    framedisplayChart.pack(fill="both", expand=True)   

    # configures title for chart
    selectLabel = Label(framedisplayChart)
    selectLabel.pack()
    selectLabel.config(text="Select a factor to edit below:")

    # creates list of factors that will be displayed
    factors = ['Name', 'Age', 'Sex', 'CP', 'TrestBPS', 'Chol', 'FBS', 'RestECG', 'Thalach', 'Exang', 'OldPeak', 'Slope', 'CA', 'Thal', 'Diagnoses']
    # generates list of desired patient data to be displayed
    infoList = infoListGen(doctor,patient)
    tree = ttk.Treeview(framedisplayChart)
        # Define the columns for the table
    columns = ['Factors', 'Value']

        # Configure the Treeview columns
    tree["columns"] = columns
    tree.heading("#0", text="Index")
    tree.column("#0", width=80)
        # Configure each column
    column_width = 80  # Adjust this value as desired
    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, width=column_width)
    for i in range (15):
        # creates new lists of each factor and their corresponding patient data and adds to chart
        newList = [factors[i], infoList[i]]
        # Insert data into the Treeview
        tree.insert('', 'end', text=i, values=newList)

        # Pack and display the Treeview
    tree.configure(height=10)  # Adjust the height value as desired
    tree.pack()
    # creates error label to display different error messages
    errorLabel = Label(framedisplayChart)
    errorLabel.pack()
    # Allows user to change specific factor
    changeButton = Button(framedisplayChart,text="Change", command=lambda: changeInfo(doctor, patient, framedisplayChart, tree, changeButton, errorLabel))
    changeButton.pack()
    # returns back to selection
    doneButton = Button(framedisplayChart, text='Done', command=lambda: changePatientPage(doctor) )
    doneButton.pack()


def changeInfo(doctor, patient, frame, tree, changebutton, errorlabel):
    '''
    Based on selection, function will display appropriate widgets to change a specific factor
    '''
    # selection made by user
    selected = tree.focus()
    if selected == '':
        # if user attempts to press change without selecting anything
        errorlabel.config(text="Please select something first.",font=("Helvetica", 16), fg="red", bg="#FFE2E1" )
    else:
        # gets the values of the selected row
        temp = tree.item(selected, 'values')
        # gets the factor that the user has chosen to edit
        factor = temp[0]
        # generates the current list of patient data
        infoList = infoListGen(doctor,patient)
        if factor == "Name" or factor == "Diagnoses":
            # displays error message if user tries to edit name or diagnoses
            errorlabel.config(text="Factor cannot be edited.",font=("Helvetica", 16), fg="red", bg="#FFE2E1" )
        else: 
            # if factor is valid, error label is removed
            errorlabel.pack_forget()
            # change button is removed so that user cannot select another factor to change in the middle of changing current factor
            changebutton.pack_forget()
            if factor == "Age":
                # displays appropriate widgets for each factor to take user input
                index = 1 # lets program know at which index of the list the change must be made
                ageLabel = Label(frame, text="Age(0-130):")
                ageLabel.pack()
                ageSP = Spinbox(frame, from_=0, to=100,) #spinbox used to make it easier for users to enter value
                ageSP.pack()
                newFactorVal = ageSP # lets program know what the new value will be at the given index
            elif factor == "Sex":
                # displays appropriate widgets for each factor to take user input
                index = 2
                sexSel = IntVar(frame)
                sexLabel = Label(frame, text="Sex:")
                sexLabel.pack()
                sexOptionZero = Radiobutton(frame, text="Female", variable=sexSel, value= 0) 
                sexOptionZero.pack()
                sexOptionOne = Radiobutton(frame, text="Male", variable=sexSel, value= 1)
                sexOptionOne.pack()
                newFactorVal = sexSel
            elif factor == "CP":
                # displays appropriate widgets for each factor to take user input
                index = 3
                cptSel = IntVar(frame)
                cptLabel = Label(frame, text="Chest pain level:")
                cptLabel.pack()
                #radiobutton used to ensure valid inputs
                cptOptionZero = Radiobutton(frame, text="0", variable=cptSel, value= 0)
                cptOptionZero.pack()
                cptOptionOne = Radiobutton(frame, text="1", variable=cptSel, value= 1)
                cptOptionOne.pack()
                cptOptionTwo = Radiobutton(frame, text="2", variable=cptSel, value= 2)
                cptOptionTwo.pack()
                cptOptionThree = Radiobutton(frame, text="3", variable=cptSel, value= 3)
                cptOptionThree.pack()
                newFactorVal = cptSel
            elif factor == "TrestBPS":
                # displays appropriate widgets for each factor to take user input
                index = 4
                bpsLabel = Label(frame, text="Resting Blood Pressure(40-200):")
                bpsLabel.pack()
                bpsSP = Spinbox(frame, from_=0, to=100)
                bpsSP.pack()
                newFactorVal = bpsSP
            elif factor == "Chol":
                # displays appropriate widgets for each factor to take user input
                index = 5
                cholLabel = Label(frame, text="Cholesterol Level(0-300):")
                cholLabel.pack()
                cholSP = Spinbox(frame, from_=0, to=250)
                cholSP.pack()
                newFactorVal = cholSP
            elif factor == "FBS":
                # displays appropriate widgets for each factor to take user input
                index = 6
                fbpsSel = StringVar(frame)
                fbpsPatient = Label(frame, text="Fasting Blood Sugar:")
                fbpsPatient.pack()
                fbsOptionZero = Radiobutton(frame, text="0", variable=fbpsSel, value= 0)
                fbsOptionZero.pack()
                fbsOptionOne = Radiobutton(frame, text="1", variable=fbpsSel, value= 1)
                fbsOptionOne.pack()
                newFactorVal = fbpsSel
            elif factor == "RestECG":
                # displays appropriate widgets for each factor to take user input
                index = 7
                restecgSel = StringVar(frame)
                restecgPatient = Label(frame, text="Resting ECG Result:")
                restecgPatient.pack()
                restecgOptionZero = Radiobutton(frame, text="0", variable=restecgSel, value= 0)
                restecgOptionZero.pack()
                restecgOptionOne = Radiobutton(frame, text="1", variable=restecgSel, value= 1)
                restecgOptionOne.pack()
                restecgOptionTwo = Radiobutton(frame, text="2", variable=restecgSel, value= 2)
                restecgOptionTwo.pack()
                newFactorVal = restecgSel
            elif factor == "Thalach":
                # displays appropriate widgets for each factor to take user input
                index = 8
                thalachLabel = Label(frame, text="Max. Heart Rate Achieved(40-250):")
                thalachLabel.pack()
                thalachSP = Spinbox(frame, from_=40, to=250)
                thalachSP.pack()  
                newFactorVal = thalachSP  
            elif factor == 'Exang':
                # displays appropriate widgets for each factor to take user input
                index = 9
                exangSel = StringVar(frame)
                exangLabel = Label(frame, text="excercise induced angia:")
                exangLabel.pack()
                exangOptionOne = Radiobutton(frame, text="Yes", variable=exangSel, value= 1)
                exangOptionOne.pack()
                exangOptionZero = Radiobutton(frame, text="No", variable=exangSel, value= 0)
                exangOptionZero.pack()
                newFactorVal = exangSel
            elif factor == 'OldPeak':
                # displays appropriate widgets for each factor to take user input
                index = 10
                oldpeakPatient = Label(frame, text="St depression induced by excercise relative to rest(0-7):")
                oldpeakPatient.pack()
                oldpeakSP = Spinbox(frame, from_=0, to=6,increment= 0.1)
                oldpeakSP.pack()
                newFactorVal = oldpeakSP
            elif factor == 'Slope':
                # displays appropriate widgets for each factor to take user input
                index = 11
                slopeSel = StringVar(frame)
                slopePatient = Label(frame, text="Slope:")
                slopePatient.pack()
                slopeOptionZero = Radiobutton(frame, text="0", variable=slopeSel, value= 0)
                slopeOptionZero.pack()
                slopeOptionOne = Radiobutton(frame, text="1", variable=slopeSel, value= 1)
                slopeOptionOne.pack()
                slopeOptionTwo = Radiobutton(frame, text="2", variable=slopeSel, value= 2)
                slopeOptionTwo.pack()
                newFactorVal = slopeSel
            elif factor == 'CA':
                # displays appropriate widgets for each factor to take user input
                index = 12
                caSel = StringVar(frame)
                caPatient = Label(frame, text="Num of vessels coloured by floroscopy:")
                caPatient.pack()
                caOptionZero = Radiobutton(frame, text="0", variable=caSel, value= 0)
                caOptionZero.pack(side='left')
                caOptionOne = Radiobutton(frame, text="1", variable=caSel, value= 1)
                caOptionOne.pack(side='left')
                caOptionTwo = Radiobutton(frame, text="2", variable=caSel, value= 2)
                caOptionTwo.pack(side='left')
                caOptionThree = Radiobutton(frame, text="3", variable=caSel, value= 3)
                caOptionThree.pack(side='left')
                newFactorVal = caSel
            elif factor == "Thal":
                # displays appropriate widgets for each factor to take user input
                index = 13
                thalSel = StringVar(frame)
                thalPatient = Label(frame, text="thal:")
                thalPatient.pack()
                thalOptionOne = Radiobutton(frame, text="normal", variable=thalSel, value= 1)
                thalOptionOne.pack()
                thalOptionTwo = Radiobutton(frame, text="fixed defect", variable=thalSel, value= 2)
                thalOptionTwo.pack()
                thalOptionThree = Radiobutton(frame, text="reversable defect", variable=thalSel, value= 3)
                thalOptionThree.pack()
                newFactorVal = thalSel
            # error label to be configured if changes are invalud
            errorLabel = Label(frame)
            errorLabel.pack()
            # takes new information to be validated and saved
            saveButton = Button(frame,text="Save", command=lambda: saveInfo(doctor, patient, newFactorVal.get(), index, infoList, errorLabel))
            saveButton.pack()


def saveInfo(doctor, patient, factor, index, list, errorLabel):
    # takes the old patient list and changes the factor value at the index given
    list[index] = factor
    # creates new list that is formatted the same as patient database ( displays doctor at begenning as well )
    newList= [doctor]
    for item in list:
        newList.append(item)
    if validatePatientData(newList[:15]) == True:
        # if changes pass validation, error label is erased
        errorLabel.pack_forget()
        # reruns diagnosis algorithim and replaces it with preveous diagnoses
        newList[15] = (neuralNetworks(newList))
        # updates database
        changePatient(newList)
        # returns to chart for users to reselect new factor
        displayChart(doctor, patient)
    else:
        # if changes are invalid, error label is displayed
        errorLabel.config(text="Invalid Input.",font=("Helvetica", 16), fg="red", bg="#FFE2E1" )


def changePatient(list):
    '''
    removes old patient information and adds updated information 
    '''
    removeOldPatient(list)
    addPatient(list)

def removeOldPatient(list):
    '''
    Reads and removed old patient information from patient database
    '''
    with open("patientDatabase.csv", 'r') as file:
       # reads database and saves to a list of all patient lists
       csv_reader = csv.reader(file)
       patients =  []
       for row in csv_reader:
           patients.append(row)
    # traverses through each patient
    for item in patients:
        # if the patient name is the same as the patient name selected to change
        if item[1] == list[1]:
            # all of that patients old data is removed
            patients.remove(item)
    # new list, without old patient data is rewriten to database
    with open("patientDatabase.csv", 'w', newline="") as file:
       csv_writer = writer(file)
       csv_writer.writerows(patients)
   
def ageList(readPatientList):
    '''
    This function takes a list of patients that have a positive diagnosis and returns 
    a dictionary of the number of people diagnosed positive in a specific age range
    '''
    # Sets all counters to 0
    valOne = 0
    valTwo = 0
    valThree = 0
    valFour = 0
    
    # Iterates through positive patients list
    for item in readPatientList:
        # Converts first index (age) from string to int, then compares
        if 0 < int(item[1]) < 25:
            # If age is from 0 to 25, first counter is increased by one
            valOne = valOne + 1
        elif 26 < int(item[1]) < 50:
            # If age is from 26 to 50, second counter is increased by one
            valTwo = valTwo + 1
        elif 51 < int(item[1]) < 75:
            # If age is from 51 to 75, third counter is increased by one
            valThree = valThree + 1
        else:
            # If age is from 76 to 130, fourth counter is increased by one
            valFour = valFour + 1
    
    # Dictionary of age range counters and keys with boundaries created
    agedict = {
        "0-25": valOne,
        "26-50": valTwo,
        "51-75": valThree,
        "76-100": valFour
    }
    # Dictionary returned
    return agedict

def genderList(readPatientList):
    '''
    This function takes a list of patients that have a positive diagnosis and returns 
    a dictionary of the number of people diagnosed positive who are female or male
    '''
    # Set both counters to 0
    valOne = 0
    valTwo = 0
           
    # Iterate through list 
    for item in readPatientList:
        # Check if index 2 (gender) is 0 or 1, i.e. female or male
        if int(item[2]) == 1:
            valOne = valOne + 1
        else:
            valTwo = valTwo + 1

    # Create dictionary of counters and gender names
    genderdict = {
        "male": valOne,
        "female": valTwo
    }
    
    # Return gender dictionary
    return genderdict

def cptList(readPatientList):
    '''
    This function takes a list of patients that have a positive diagnosis and returns 
    a dictionary of the number of people diagnosed with a specific chest pain type
    '''
    # Sets counters to 0
    valOne = 0
    valTwo = 0
    valThree = 0
    valFour = 0
          
    # Iterates through list  
    for item in readPatientList:
        # Checks index 3 (type) and convert to int to increase counter
        if int(item[3]) == 0:
            valOne = valOne + 1
        elif int(item[3]) == 1:
            valTwo = valTwo + 1
        elif int(item[3]) == 2:
            valThree = valThree + 1
        else:
            valFour = valFour + 1
    
    # Creates dict with counters and chest pain type label numbers
    cptdict = {
        "0": valOne,
        "1": valTwo,
        "2": valThree,
        "3": valFour
    }
    
    # Returns dictionary
    return cptdict

def rbpList(readPatientList):
    '''
    This function takes a list of patients that have a positive diagnosis and returns 
    a dictionary of the number of people diagnosed positive in a specific resting blood pressure range
    '''
    # Set counters to 0
    valOne = 0
    valTwo = 0
    valThree = 0
    valFour = 0
    
    # Iterate through list
    for item in readPatientList:
        # Checks which resting blood pressure range each positive patient is in and add to
        # associated counter
        if 40 < int(item[4]) < 80:
            valOne = valOne + 1
        elif 81 < int(item[4]) < 120:
            valTwo = valTwo + 1
        elif 121 < int(item[4]) < 160:
            valThree = valThree + 1
        else:
            valFour = valFour + 1
    
    # Creates dictionary with counters and range labels
    rbpdict = {
        "40-80": valOne,
        "81-120": valTwo,
        "121-160": valThree,
        "161-200": valFour
    }
    
    # Returns dictionary
    return rbpdict
     
def graphMaker(feature, readPatientList):
    '''
    Takes string feature and positive patients list as input and has no return value.
    Function creates a new window with a relevant graph. 
    '''
    # Checks if user selected age to be graphed
    if feature == "age":
        # Gets dictionary for ages from ageList function
        dict = ageList(readPatientList)
        # creating the dataset from dictionary
        keysList = list(dict.keys())
        data = {keysList[0]:dict.get(keysList[0]), keysList[1]:dict.get(keysList[1]),
                keysList[2]:dict.get(keysList[2]), keysList[3]:dict.get(keysList[3])}
        courses = list(data.keys())
        values = list(data.values())
        
        # Creates figure
        fig = plt.figure(figsize = (10, 5))
        
        # creating the bar plot
        plt.bar(courses, values, color ='#127ca1',
                width = 0.4)
        
        # Set x and y axis labels
        plt.xlabel("Age range (in years)")
        plt.ylabel("Number of patients in the range with a POSITIVE diagnosis")
        plt.title("Age Analysis Regarding Heart Disease")
        plt.show()
    
    elif feature == "gender":
        # Checks if user selected gender to be graphed
        # Gets dictionary for gender from genderList function
        dict = genderList(readPatientList)
        # creating the dataset fron dictionary
        keysList = list(dict.keys())
        data = {keysList[0]:dict.get(keysList[0]), keysList[1]:dict.get(keysList[1])}
        courses = list(data.keys())
        values = list(data.values())
        
        fig = plt.figure(figsize = (10, 5))
        
        # creating the bar plot
        plt.bar(courses, values, color ='#127ca1',
                width = 0.4)
        
        # Set x and y axis labels
        plt.xlabel("Gender")
        plt.ylabel("Number of patients with a POSITIVE diagnosis")
        plt.title("Gender Analysis Regarding Heart Disease")
        plt.show()
        
    elif feature == "chest pain type":
        # Checks if user selected chest pain type to be graphed
        # Gets dictionary for cpt from cptList function
        dict = cptList(readPatientList)
        # creating the dataset from dictionary
        keysList = list(dict.keys())
        data = {keysList[0]:dict.get(keysList[0]), keysList[1]:dict.get(keysList[1]),
                keysList[2]:dict.get(keysList[2]), keysList[3]:dict.get(keysList[3])}
        courses = list(data.keys())
        values = list(data.values())
        
        fig = plt.figure(figsize = (10, 5))
        
        # creating the bar plot
        plt.bar(courses, values, color ='#127ca1',
                width = 0.4)
        
        # Set x and y axis labels
        plt.xlabel("Chest Pain Type (0-Typical Angina, 1-Atypical Angina, 2-Nonanginal Pain, 3-Asymptomatic)")
        plt.ylabel("Number of patients with a POSITIVE diagnosis")
        plt.title("Chest Pain Analysis Regarding Heart Disease")
        plt.show()
        
    else:
        # Checks if user selected resting blood pressure to be graphed
        # Gets dictionary for rbp from rbpList function
        dict = rbpList(readPatientList)
        # creating the dataset from dict
        keysList = list(dict.keys())
        data = {keysList[0]:dict.get(keysList[0]), keysList[1]:dict.get(keysList[1]),
                keysList[2]:dict.get(keysList[2]), keysList[3]:dict.get(keysList[3])}
        courses = list(data.keys())
        values = list(data.values())
        
        fig = plt.figure(figsize = (10, 5))
        
        # creating the bar plot
        plt.bar(courses, values, color ='#127ca1',
                width = 0.4)
        
        # Set x and y axis labels
        plt.xlabel("Resting Blood Pressure (mmHg)")
        plt.ylabel("Number of patients with a POSITIVE diagnosis")
        plt.title("Blood Pressure Analysis Regarding Heart Disease")
        plt.show()
        
def graphCall(usr):
    '''
    This function is called to display graph page and evenutally call graphMaker for the graph
    Takes doctor's name string as a parameter and no return values.
    '''
    # Clears previous page and sets new frame for graph page
    clearPage()
    frameGraphPatientPage = Frame(frameMain)
    frameGraphPatientPage.pack(fill="both", expand=True)

    # Collects all patients that are under doctor name passed as parameter
    totalList = collectPatients(usr)
    # Creates empty patient list that is to save all diagnosed positive patients
    patientsList = []
    # Iterate through all patients
    for item in totalList:
        # Check if diagnosis is positive, if so then append to positive patients list
        if item[-1] == "Positive":
            patientsList.append(item)
        else:
            continue

    # If doctor have no patients then display relevant message and optiond
    if not totalList:
        errorLabel = Label(frameGraphPatientPage, text="You have no patients to graph")
        errorLabel.pack()
        addButton = Button(frameGraphPatientPage, text="Add Patient", fg='#127ca1', command=lambda: addPatientPage(usr))
        addButton.pack()
    # If doctor has patients, then prompt user to input the feature they would like to graph
    else:
        graphLabel = Label(frameGraphPatientPage, text="Which feature would you like to plot?")
        graphLabel.pack() 

        graphButtonWidth = 15
        
        # Each button for feature calls the graphMaker on click with the
        # associated feature name as a string parameter and the positive patients list
        # as another parameter.
        addButton = Button(frameGraphPatientPage, text="Age", fg='#127ca1', width=graphButtonWidth, command=lambda: graphMaker("age", patientsList))
        addButton.pack(pady=10)
        
        addButton = Button(frameGraphPatientPage, text="Gender", fg='#127ca1', width=graphButtonWidth, command=lambda: graphMaker("gender", patientsList))
        addButton.pack(pady=10)
        
        addButton = Button(frameGraphPatientPage, text="Chest Pain Type", fg='#127ca1', width=graphButtonWidth, command=lambda: graphMaker("chest pain type", patientsList))
        addButton.pack(pady=10)
        
        addButton = Button(frameGraphPatientPage, text="Resting Blood Pressure", fg='#127ca1', width=graphButtonWidth, command=lambda: graphMaker("rbp", patientsList))
        addButton.pack(pady=10)

        createBackButton = Button(frameMain, text="← Back", command=lambda: homePage(usr))
        createBackButton.pack(pady=30)
    
# Main Code
win = Tk()
win.title("Hospital System")
win.geometry("700x500")

# Doesn't allow the screen to be resized:
# win.resizable(0, 0)

frameMain = Frame(win) #All other created frames are children of this frame, making them contained under frameMain
frameMain.pack(expand=True, anchor="n") 
# program runs beginning from login page
loginPage()

win.mainloop()