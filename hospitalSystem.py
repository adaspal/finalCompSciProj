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
import matplotlib.pyplot as plt
from pylab import cm
import warnings

import pandas as pd
import opendatasets as od
import numpy as np

warnings.filterwarnings("ignore")

# scikit-learn imports
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier

def clearPage():
    for widget in frameMain.winfo_children():
        widget.destroy()

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
    createAccountButton.pack()

    # errorLabel = Label(frameMain, font=("Helvetica", 16), fg="red")  # Create the error label to config under validation so that it only appears once

def createAccountPage():
    ''' Creates create account page'''
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
    loginLabel.pack(pady=30)  # padding from the top

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
    createAccountButton.pack(pady=25)

def homePage(usr):
    ''' Creates home page'''
    clearPage()
    # Create home page
    frameHome = Frame(frameMain)
    frameHome.pack(fill="both", expand=True)

    homeLabel = Label(frameHome, text=f"Welcome " + usr, font=('Helvetica', 36, "bold"))
    homeLabel.pack()

    viewButton = Button(frameHome, text="View Patient", fg='blue', command=lambda: viewPatientPage(usr))
    viewButton.pack(pady=20)
    addButton = Button(frameHome, text="Add Patient", fg='blue', command=lambda: addPatientPage(usr))
    addButton.pack(pady=20)
    changeButton = Button(frameHome, text="Change Patient", fg='blue', command=lambda: changePatientPage(usr))
    changeButton.pack(pady=20)
    graphButton = Button(frameHome, text="Graph Data", fg='blue', command=lambda: graphCall(usr))
    graphButton.pack(pady=20)
    signOutButton = Button(frameHome, text="Sign Out", fg='blue', command=lambda: signOut())
    signOutButton.pack(pady=20)
    
def signOut():
    #creating this function to run the login page makes the program more modular and easy to maintain
    loginPage()

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
        newAccountList = [createdUsername, createdPassword]
        with open("doctorCredentials.csv", "a+", newline='') as file:
            csv_writer = writer(file)
            csv_writer.writerow(newAccountList)
        usr = createdUsername             
        homePage(usr)
    else:
        errorLabel2 = Label(frameMain, text="X -This account is invalid or already exists. Please try again.", font=("Helvetica", 16), fg="red", bg="#FFE2E1")
        errorLabel2.pack(pady=10)
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
    if validateCredentials(username, password):
        usr = username
        homePage(usr)
    else:
        print("Try again")
        if not hasattr(login, 'errorLabel'):  # Check if errorLabel attribute exists so it does not create a new frame
            login.errorLabel = Label(frameMain, font=("Helvetica", 16), fg="red", bg="#FFE2E1")
            login.errorLabel.pack(pady=15)
        login.errorLabel.config(text="X -Incorrect username and/or password. Please try again.")

def collectPatients(usr):
    patients = []
    with open("patientDatabase.csv", 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row[0] == usr:
                patients.append(row[1:])
    return patients

def viewPatientPage(usr):
    clearPage()
    frameviewPatientPage = Frame(frameMain)
    frameviewPatientPage.pack(fill="both", expand=True)

    patientsList = collectPatients(usr)

    if not patientsList:
        errorLabel = Label(frameviewPatientPage, text="You have no patients to view")
        errorLabel.pack()
        addButton = Button(frameviewPatientPage, text="Add Patient", fg='blue', command=lambda: addPatientPage(usr))
        addButton.pack()
    else:
        tree = ttk.Treeview(frameviewPatientPage, xscrollcommand=True)

        # Define the columns for the table
        columns = ['Name', 'Age', 'Sex', 'CP', 'TrestBPS', 'Chol', 'FBS', 'RestECG', 'Thalach', 'Exang', 'OldPeak', 'Slope', 'CA', 'Thal', 'Diagnoses']

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

def addPatientPage(usr):
    clearPage()
    frameaddPatientPage = Frame(frameMain)
    frameaddPatientPage.pack(fill="both", expand=True)
    addPLabel = Label(frameaddPatientPage, text="Add Your patient " + usr, font=('Helvetica', 36, "bold"))
    addPLabel.pack()

    patientNameLabel = Label(frameaddPatientPage, text="Patient Name:")
    patientNameLabel.pack()
    entryPatient = Entry(frameaddPatientPage)
    entryPatient.pack()

    ageLabel = Label(frameaddPatientPage, text="Age:")
    ageLabel.pack()
    ageSP = Spinbox(frameaddPatientPage, from_=0, to=100)
    ageSP.pack()

    sexSel = StringVar(frameaddPatientPage)
    sexSel.set("Sex: ")
    sexMenu = OptionMenu(frameaddPatientPage, sexSel, "Male","Female" )
    sexMenu.pack()

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
    
    bpsLabel = Label(frameaddPatientPage, text="Resting Blood Pressure:")
    bpsLabel.pack()
    bpsSP = Spinbox(frameaddPatientPage, from_=0, to=100)
    bpsSP.pack()

    nextButton = Button(frameaddPatientPage, text="Next", fg='blue', command=lambda: addPatientPageTwo(usr, entryPatient.get(),ageSP.get(), sexSel.get(), cptSel.get(), bpsSP.get() ))
    nextButton.pack()


def addPatientPageTwo(doctor, patient, age, sex, cpt, rbp):
    if sex == "Male":
        sex = 1
    else: 
        sex = 0
    patientHealthList= [doctor, patient, age, sex, cpt, rbp]
    if validatePatientData(patientHealthList) == True:
        clearPage()
        frameaddPatientPageTwo = Frame(frameMain)
        frameaddPatientPageTwo.pack(fill="both", expand=True)
        
        cholLabel = Label(frameaddPatientPageTwo, text="Cholesterol Level:")
        cholLabel.pack()
        cholSP = Spinbox(frameaddPatientPageTwo, from_=0, to=250)
        cholSP.pack()

        fbpsSel = StringVar(frameaddPatientPageTwo)
        fbpsPatient = Label(frameaddPatientPageTwo, text="Fasting Blood Sugar:")
        fbpsPatient.pack()
        fbsOptionZero = Radiobutton(frameaddPatientPageTwo, text="0", variable=fbpsSel, value= 0)
        fbsOptionZero.pack()
        fbsOptionOne = Radiobutton(frameaddPatientPageTwo, text="1", variable=fbpsSel, value= 1)
        fbsOptionOne.pack()

        restecgSel = StringVar(frameaddPatientPageTwo)
        restecgPatient = Label(frameaddPatientPageTwo, text="Resting ECG Result:")
        restecgPatient.pack()
        restecgOptionZero = Radiobutton(frameaddPatientPageTwo, text="0", variable=restecgSel, value= 0)
        restecgOptionZero.pack()
        restecgOptionOne = Radiobutton(frameaddPatientPageTwo, text="1", variable=restecgSel, value= 1)
        restecgOptionOne.pack()
        restecgOptionTwo = Radiobutton(frameaddPatientPageTwo, text="2", variable=restecgSel, value= 2)
        restecgOptionTwo.pack()
        
        thalLabel = Label(frameaddPatientPageTwo, text="Max. Heart Rate Achieved:")
        thalLabel.pack()
        thalSP = Spinbox(frameaddPatientPageTwo, from_=40, to=250)
        thalSP.pack()

        exangSel = StringVar(frameaddPatientPageTwo)
        exangLabel = Label(frameaddPatientPageTwo, text="excercise induced angia:")
        exangLabel.pack()
        exangOptionOne = Radiobutton(frameaddPatientPageTwo, text="Yes", variable=exangSel, value= 1)
        exangOptionOne.pack()
        exangOptionZero = Radiobutton(frameaddPatientPageTwo, text="No", variable=exangSel, value= 0)
        exangOptionZero.pack()

        nextButton = Button(frameaddPatientPageTwo, text="Next", fg='blue', command=lambda: addPatientPageThree(patientHealthList,cholSP.get(), fbpsSel.get(), restecgSel.get(), thalSP.get(), exangSel.get() ))
        nextButton.pack()
    else:
        print("Error")

def addPatientPageThree(patientHealthList, chol,fbs,restecg,thalach,exang):
    patientHealthList.extend([chol,fbs,restecg,thalach,exang])
    if validatePatientData(patientHealthList) == True:
        clearPage()
        frameaddPatientPageThree = Frame(frameMain)
        frameaddPatientPageThree.pack(fill="both", expand=True)

        oldpeakPatient = Label(frameaddPatientPageThree, text="St depression induced by excercise relative to rest:")
        oldpeakPatient.pack()
        oldpeakSP = Spinbox(frameaddPatientPageThree, from_=0, to=6,increment= 0.1)
        oldpeakSP.pack()

        slopeSel = StringVar(frameaddPatientPageThree)
        slopePatient = Label(frameaddPatientPageThree, text="Slope:")
        slopePatient.pack()
        slopeOptionZero = Radiobutton(frameaddPatientPageThree, text="0", variable=slopeSel, value= 0)
        slopeOptionZero.pack()
        slopeOptionOne = Radiobutton(frameaddPatientPageThree, text="1", variable=slopeSel, value= 1)
        slopeOptionOne.pack()
        slopeOptionTwo = Radiobutton(frameaddPatientPageThree, text="2", variable=slopeSel, value= 2)
        slopeOptionTwo.pack()

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

        thalSel = StringVar(frameaddPatientPageThree)
        thalPatient = Label(frameaddPatientPageThree, text="thal:")
        thalPatient.pack()
        thalOptionOne = Radiobutton(frameaddPatientPageThree, text="normal", variable=thalSel, value= 1)
        thalOptionOne.pack()
        thalOptionTwo = Radiobutton(frameaddPatientPageThree, text="fixed defect", variable=thalSel, value= 2)
        thalOptionTwo.pack()
        thalOptionThree = Radiobutton(frameaddPatientPageThree, text="reversable defect", variable=thalSel, value= 3)
        thalOptionThree.pack()

        
        saveButton = Button(frameaddPatientPageThree, text="Save", fg='blue', command=lambda: diagnosePatient(patientHealthList,oldpeakSP.get(), slopeSel.get(), caSel.get(), thalSel.get() ))
        saveButton.pack()
    else:
        print("Error")
      
def validatePatientData(patientInfoList):
    i = 0
    for item in patientInfoList[2:]:
        if isinstance(item, str):
            if item.isdigit() == True or isfloat(item) == True:
                if i == 0: #age
                    if 0 < int(item) < 130:
                        continue
                    else:
                        return False
                if i == 3: #rbp
                    if 0 < int(item) < 130:
                        continue
                    else:
                        return False
                if i == 4:
                    if 0 < int(item) < 300:
                        continue
                    else:
                        return False
                if i == 7:
                    if 50 < int(item) < 250:
                        continue
                    else:
                        return False
                if i == 9:
                    if 0 < float(item) < 7:
                        continue
                    else:
                        return False
            else:
                return False
        else:
            continue
        
    return True

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def diagnosePatient(patientHealthList, oldpeak, slope, ca, thal):
    patientHealthList.extend([oldpeak, slope, ca, thal])
    
    if validatePatientData(patientHealthList) == True:
        patientHealthList.append(neuralNetworks(patientHealthList))
        addPatient(patientHealthList)
    else:
        print("Error")
    
def addPatient(list):
    with open("patientDatabase.csv", 'a', newline="") as file:
       csv_writer = writer(file)
       csv_writer.writerow(list)


def neuralNetworks(list): 
    data = pd.read_csv('heart.csv')

    # Split train data
    y=data.target
    x=data.drop('target',axis=1)

    sample_train, sample_val, labels_train, labels_val = train_test_split(x,y,test_size=0.4, random_state=42)

    sample_train = sample_train.to_numpy()

    sample_val = sample_val.to_numpy()

    # Standardize
    ss = StandardScaler()
    sample_train = ss.fit_transform(sample_train)
    sample_val = ss.transform(sample_val)
    #sample_test = ss.transform(sample_test)

    # Reduce dimensions 
    N_DIM = 13
    pca = PCA(n_components=N_DIM)
    sample_train = pca.fit_transform(sample_train)
    sample_val = pca.transform(sample_val)
    #sample_test = pca.transform(sample_test)

    nn = MLPClassifier()
    nn.fit(sample_train, labels_train)
    nnScore = nn.score(sample_val, labels_val) * 100
    nnScore = round(nnScore, 2)
    print(f"NN test score: {nnScore}" + "%")


    age = int(list[2])
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
    features = np.array([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])
    prediction = nn.predict(features)
    prediction = prediction[0]
    if prediction == 0:
        prediction = 'No'
    else:
        prediction = 'Yes'
    return prediction

def changePatientPage(usr):
    # clears previous page and creates page
    clearPage()
    framechangePatient = Frame(frameMain)
    framechangePatient.pack(fill="both", expand=True)

    # creates list of patients that doctors can select
    patientSel = StringVar(framechangePatient)
    patientSel.set("Patient: ")
    patientNameList = []
    for item in collectPatients(usr):
        patientNameList.append(item[0])
    # if list is empty, doctor cannot change any patients
    if not patientNameList:
        errorLabel = Label(framechangePatient, text="You have no patients to change.")
        errorLabel.pack()
        addButton = Button(framechangePatient, text="Add patient", fg='blue', command=lambda: addPatientPage(usr))
        addButton.pack(side='left')
        homeButton = Button(framechangePatient,text="Home", command=lambda: homePage(usr))
        homeButton.pack(side='right')
    else: # if doctor has patients

        # option menu for patients to select from
        patientSel = StringVar(framechangePatient)
        patientSel.set("Patient: ")
        # once selected, display current information
        patientMenu = OptionMenu(framechangePatient, patientSel,*patientNameList, command= lambda x: displayLabel(usr, patientSel.get(), framechangePatient))
        patientMenu.pack()

def infoListGen(doctor, patient):
    for item in collectPatients(doctor):
        if item[0] == patient:
            infoList = item
    return infoList
    

def displayLabel(doctor, patient, frame):
    factors = ['Name', 'Age', 'Sex', 'CP', 'TrestBPS', 'Chol', 'FBS', 'RestECG', 'Thalach', 'Exang', 'OldPeak', 'Slope', 'CA', 'Thal', 'Diagnoses']
    infoList = infoListGen(doctor,patient)
    tree = ttk.Treeview(frame)

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
        newList = [factors[i], infoList[i]]
        # Insert data into the Treeview
        tree.insert('', 'end', values=newList)

        # Pack and display the Treeview
    tree.pack()
    changeButton = Button(frame,text="Change", command=lambda: changeInfo(doctor, patient, frame, tree, changeButton))
    changeButton.pack()


def changeInfo(doctor, patient, frame, display, button):
    selected = display.focus()
    if selected == '':
        print ("select something")
    else:
        temp = display.item(selected, 'values')
        factor = temp[0]
        infoList = infoListGen(doctor,patient)
        if factor == "Age":
            index = 1
            ageLabel = Label(frame, text="Age:")
            ageLabel.pack()
            ageSP = Spinbox(frame, from_=0, to=100,)
            ageSP.pack()
            newFactorVal = ageSP
            widgets = [ageSP, ageLabel, button, display]
        elif factor == "Sex":
            index = 2
            sexSel = IntVar(frame)
            sexLabel = Label(frame, text="Sex:")
            sexLabel.pack()
            sexOptionZero = Radiobutton(frame, text="Female", variable=sexSel, value= 0)
            sexOptionZero.pack()
            sexOptionOne = Radiobutton(frame, text="Male", variable=sexSel, value= 1)
            sexOptionOne.pack()
            newFactorVal = sexSel
            widgets = [sexLabel,sexOptionOne,sexOptionZero, button , display]
        elif factor == "CP":
            index = 3
            cptSel = IntVar(frame)
            cptLabel = Label(frame, text="Chest pain level:")
            cptLabel.pack()
            cptOptionZero = Radiobutton(frame, text="0", variable=cptSel, value= 0)
            cptOptionZero.pack()
            cptOptionOne = Radiobutton(frame, text="1", variable=cptSel, value= 1)
            cptOptionOne.pack()
            cptOptionTwo = Radiobutton(frame, text="2", variable=cptSel, value= 2)
            cptOptionTwo.pack()
            cptOptionThree = Radiobutton(frame, text="3", variable=cptSel, value= 3)
            cptOptionThree.pack()
            newFactorVal = cptSel
            widgets = [cptLabel, cptOptionZero, cptOptionOne,cptOptionTwo, cptOptionThree, button, display]
        elif factor == "TrestBPS":
            index = 4
            bpsLabel = Label(frame, text="Resting Blood Pressure:")
            bpsLabel.pack()
            bpsSP = Spinbox(frame, from_=0, to=100)
            bpsSP.pack()
            newFactorVal = bpsSP
            widgets = [bpsLabel, bpsSP, button, display]
        elif factor == "Chol":
            index = 5
            cholLabel = Label(frame, text="Cholesterol Level:")
            cholLabel.pack()
            cholSP = Spinbox(frame, from_=0, to=250)
            cholSP.pack()
            newFactorVal = cholSP
            widgets = [cholLabel, cholSP, button, display]
        elif factor == "FBS":
            index = 6
            fbpsSel = StringVar(frame)
            fbpsPatient = Label(frame, text="Fasting Blood Sugar:")
            fbpsPatient.pack()
            fbsOptionZero = Radiobutton(frame, text="0", variable=fbpsSel, value= 0)
            fbsOptionZero.pack()
            fbsOptionOne = Radiobutton(frame, text="1", variable=fbpsSel, value= 1)
            fbsOptionOne.pack()
            newFactorVal = fbpsSel
            widgets = [fbpsPatient,fbsOptionOne,fbsOptionZero, button, display]
        elif factor == "RestECG":
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
            widgets = [restecgPatient, restecgOptionZero,restecgOptionOne,restecgOptionTwo, button, display]
        elif factor == "Thalach":
            index = 8
            thalachLabel = Label(frame, text="Max. Heart Rate Achieved:")
            thalachLabel.pack()
            thalachSP = Spinbox(frame, from_=40, to=250)
            thalachSP.pack()  
            newFactorVal = thalachSP
            widgets = [thalachLabel, thalachSP, button, display]     
        elif factor == 'Exang':
            index = 9
            exangSel = StringVar(frame)
            exangLabel = Label(frame, text="excercise induced angia:")
            exangLabel.pack()
            exangOptionOne = Radiobutton(frame, text="Yes", variable=exangSel, value= 1)
            exangOptionOne.pack()
            exangOptionZero = Radiobutton(frame, text="No", variable=exangSel, value= 0)
            exangOptionZero.pack(side='left')
            newFactorVal = exangSel
            widgets = [exangLabel, exangOptionOne,exangOptionZero, button, display]
    
        elif factor == 'OldPeak':
            index = 10
            oldpeakPatient = Label(frame, text="St depression induced by excercise relative to rest:")
            oldpeakPatient.pack()
            oldpeakSP = Spinbox(frame, from_=0, to=6,increment= 0.1)
            oldpeakSP.pack()
            newFactorVal = oldpeakSP
            widgets = [oldpeakPatient,oldpeakSP,display,button]
        elif factor == 'Slope':
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
            widgets = [slopePatient,slopeOptionZero,slopeOptionOne,slopeOptionTwo, display, button]
        elif factor == 'CA':
            index = 12
            caSel = StringVar(frame)
            caPatient = Label(frame, text="Num of vessels coloured by floroscopy:")
            caPatient.pack()
            caOptionZero = Radiobutton(frame, text="0", variable=caSel, value= 0)
            caOptionZero.pack()
            caOptionOne = Radiobutton(frame, text="1", variable=caSel, value= 1)
            caOptionOne.pack()
            caOptionTwo = Radiobutton(frame, text="2", variable=caSel, value= 2)
            caOptionTwo.pack()
            caOptionThree = Radiobutton(frame, text="3", variable=caSel, value= 3)
            caOptionThree.pack()
            newFactorVal = caSel
            widgets = [caPatient, caOptionOne, caOptionTwo, caOptionZero, caOptionThree, display,button]
        elif factor == "Thal":
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
            widgets = [thalPatient,thalOptionOne, thalOptionTwo, thalOptionThree]


        saveButton = Button(frame,text="save", command=lambda: saveInfo(doctor, patient, frame, newFactorVal.get(), index, infoList, widgets, saveButton))
        saveButton.pack()

def hideMe(widgets,button):
    for item in widgets:
        item.pack_forget()
    button.pack_forget()

def saveInfo(doctor, patient, frame, factor, index, list, widgets, saveButton):
    list[index] = factor
    newList= [doctor]
    for item in list:
        newList.append(item)
    if validatePatientData(newList[:15]) == True:
        hideMe(widgets, saveButton)
        newList[15] = (neuralNetworks(newList))
        changePatient(newList)
        displayLabel(doctor, patient, frame)
    else:
        print("error")

def addPatient(list):
    with open("patientDatabase.csv", 'a', newline="") as file:
       csv_writer = writer(file)
       csv_writer.writerow(list)

def changePatient(list):
    removeOldPatient(list)
    addPatient(list)

def removeOldPatient(list):
    with open("patientDatabase.csv", 'r') as file:
       csv_reader = csv.reader(file)
       patients =  []
       for row in csv_reader:
           patients.append(row)
    for item in patients:
        if item[1] == list[1]:
            patients.remove(item)
    with open("patientDatabase.csv", 'w', newline="") as file:
       csv_writer = writer(file)
       csv_writer.writerows(patients)
   
def ageList(readPatientList):
    valOne = 0
    valTwo = 0
    valThree = 0
    valFour = 0
    
    for item in readPatientList:
        print(item[1])
        if 0 < int(item[1]) < 25:
            valOne = valOne + 1
        elif 26 < int(item[1]) < 50:
            valTwo = valTwo + 1
        elif 51 < int(item[1]) < 75:
            valThree = valThree + 1
        else:
            valFour = valFour + 1
    
    agedict = {
        "0-25": valOne,
        "26-50": valTwo,
        "51-75": valThree,
        "76-100": valFour
    }
    return agedict

def genderList(readPatientList):
    valOne = 0
    valTwo = 0
            
    for item in readPatientList:
        if int(item[2]) == 1:
            valOne = valOne + 1
        else:
            valTwo = valTwo + 1

    genderdict = {
        "male": valOne,
        "female": valTwo
    }
    
    return genderdict

def cptList(readPatientList):
    valOne = 0
    valTwo = 0
    valThree = 0
    valFour = 0
            
    for item in readPatientList:
        if int(item[3]) == 0:
            valOne = valOne + 1
        elif int(item[3]) == 1:
            valTwo = valTwo + 1
        elif int(item[3]) == 2:
            valThree = valThree + 1
        else:
            valFour = valFour + 1
    
    cptdict = {
        "0": valOne,
        "1": valTwo,
        "2": valThree,
        "3": valFour
    }
    
    return cptdict

def rbpList(readPatientList):
    valOne = 0
    valTwo = 0
    valThree = 0
    valFour = 0
    
    for item in readPatientList:
        if 40 < int(item[4]) < 80:
            valOne = valOne + 1
        elif 81 < int(item[4]) < 120:
            valTwo = valTwo + 1
        elif 121 < int(item[4]) < 160:
            valThree = valThree + 1
        else:
            valFour = valFour + 1
    
    rbpdict = {
        "40-80": valOne,
        "81-120": valTwo,
        "121-160": valThree,
        "161-200": valFour
    }
    
    return rbpdict
     
def graphMaker(feature, readPatientList):
    if feature == "age":
        dict = ageList(readPatientList)
        # creating the dataset
        keysList = list(dict.keys())
        data = {keysList[0]:dict.get(keysList[0]), keysList[1]:dict.get(keysList[1]),
                keysList[2]:dict.get(keysList[2]), keysList[3]:dict.get(keysList[3])}
        courses = list(data.keys())
        values = list(data.values())
        
        fig = plt.figure(figsize = (10, 5))
        
        # creating the bar plot
        plt.bar(courses, values, color ='blue',
                width = 0.4)
        
        plt.xlabel("Age range (in years)")
        plt.ylabel("Number of patients in the range with a YES diagnosis")
        plt.title("Age Analysis Regarding Heart Disease")
        plt.show()
    
    elif feature == "gender":
        dict = genderList(readPatientList)
        # creating the dataset
        keysList = list(dict.keys())
        data = {keysList[0]:dict.get(keysList[0]), keysList[1]:dict.get(keysList[1])}
        courses = list(data.keys())
        values = list(data.values())
        
        fig = plt.figure(figsize = (10, 5))
        
        # creating the bar plot
        plt.bar(courses, values, color ='blue',
                width = 0.4)
        
        plt.xlabel("Gender")
        plt.ylabel("Number of patients with a YES diagnosis")
        plt.title("Gender Analysis Regarding Heart Disease")
        plt.show()
        
    elif feature == "chest pain type":
        dict = cptList(readPatientList)
        # creating the dataset
        keysList = list(dict.keys())
        data = {keysList[0]:dict.get(keysList[0]), keysList[1]:dict.get(keysList[1]),
                keysList[2]:dict.get(keysList[2]), keysList[3]:dict.get(keysList[3])}
        courses = list(data.keys())
        values = list(data.values())
        
        fig = plt.figure(figsize = (10, 5))
        
        # creating the bar plot
        plt.bar(courses, values, color ='blue',
                width = 0.4)
        
        plt.xlabel("Chest Pain Type (0-Typical Angina, 1-Atypical Angina, 2-Nonanginal Pain, 3-Asymptomatic)")
        plt.ylabel("Number of patients with a YES diagnosis")
        plt.title("Chest Pain Analysis Regarding Heart Disease")
        plt.show()
        
    else:
        dict = rbpList(readPatientList)
        # creating the dataset
        keysList = list(dict.keys())
        data = {keysList[0]:dict.get(keysList[0]), keysList[1]:dict.get(keysList[1]),
                keysList[2]:dict.get(keysList[2]), keysList[3]:dict.get(keysList[3])}
        courses = list(data.keys())
        values = list(data.values())
        
        fig = plt.figure(figsize = (10, 5))
        
        # creating the bar plot
        plt.bar(courses, values, color ='blue',
                width = 0.4)
        
        plt.xlabel("Resting Blood Pressure (mmHg)")
        plt.ylabel("Number of patients with a YES diagnosis")
        plt.title("Blood Pressure Analysis Regarding Heart Disease")
        plt.show()
        
def graphCall(usr):
    clearPage()
    frameGraphPatientPage = Frame(frameMain)
    frameGraphPatientPage.pack(fill="both", expand=True)

    patientsList = collectPatients(usr)

    if not patientsList:
        errorLabel = Label(frameGraphPatientPage, text="You have no patients to graph")
        errorLabel.pack()
        addButton = Button(frameGraphPatientPage, text="Add Patient", fg='blue', command=lambda: addPatientPage(usr))
        addButton.pack()
    else:
        graphLabel = Label(frameGraphPatientPage, text="Which feature would you like to plot?")
        graphLabel.pack() 
        
        addButton = Button(frameGraphPatientPage, text="Age", fg='blue', command=lambda: graphMaker("age", patientsList))
        addButton.pack()
        
        addButton = Button(frameGraphPatientPage, text="Gender", fg='blue', command=lambda: graphMaker("gender", patientsList))
        addButton.pack()
        
        addButton = Button(frameGraphPatientPage, text="Chest Pain Type", fg='blue', command=lambda: graphMaker("chest pain type", patientsList))
        addButton.pack()
        
        addButton = Button(frameGraphPatientPage, text="Resting Blood Pressure", fg='blue', command=lambda: graphMaker("rbp", patientsList))
        addButton.pack()
    
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