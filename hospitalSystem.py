import csv
from csv import writer
from tkinter import *
# General imports
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

    loginButton = Button(frameLogin, text="Sign in", command=lambda:login(entryUsername.get(), entryPassword.get()))
    loginButton.pack(pady=25)
    
    createAccountButton = Button(frameLogin, text="Don't Have an Account? Click Here", fg='blue', command=createAccountPage)
    createAccountButton.pack(pady=20)

    # errorLabel = Label(frameMain, font=("Helvetica", 16), fg="red")  # Create the error label to config under validation so that it only appears once

def createAccountPage():
    ''' Creates create account page'''
    clearPage()
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

def homePage(usr):
    ''' Creates home page'''
    clearPage()
    # Create home page
    frameHome = Frame(frameMain, bg="red")
    frameHome.pack(fill="both", expand=True)

    homeLabel = Label(frameHome, text=f"WELCOME " + usr, bg="red")
    homeLabel.pack()

    viewButton = Button(frameHome, text="view patient", fg='blue', command=lambda: viewPatientPage(usr))
    viewButton.pack(pady=30)
    addButton = Button(frameHome, text="Add patient", fg='blue', command=lambda: addPatientPage(usr))
    addButton.pack(pady=40)
    changeButton = Button(frameHome, text="Change patient", fg='blue', command=lambda: changePatientPage(usr))
    changeButton.pack(pady=40)
    

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
        errorLabel2.pack(pady=50)
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
        usr = username
        homePage(usr)
        #return username #find a way to assign a variable to the validated username in the main code, so that it can be passed through other functions
    else:
        print("Try again")
        #errorLabel = Label(frameMain, text="X -Incorrect username and/or password. Please try again.", font=("Helvetica", 16), fg="red", bg="#FFE2E1")
        #errorLabel.pack(pady=5)

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
        errorLabel = Label(viewPatientPage, text="You have no patients to view")
        errorLabel.pack()
        addButton = Button(frameviewPatientPage, text="AddPatient", fg='blue', command=lambda: addPatientPage(usr))
        addButton.pack()




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
    ageSP = Spinbox(frameaddPatientPage, from_=0, to=100,)
    ageSP.pack()

    sexSel = StringVar(frameaddPatientPage)
    sexSel.set("Sex: ")
    sexMenu = OptionMenu(frameaddPatientPage, sexSel, "Male","Female" )
    sexMenu.pack()

    cptSel = StringVar(frameaddPatientPage)
    cptOptionZero = Radiobutton(frameaddPatientPage, text="0", variable=cptSel, value= 0)
    cptOptionZero.pack()
    cptOptionOne = Radiobutton(frameaddPatientPage, text="1", variable=cptSel, value= 1)
    cptOptionOne.pack()
    cptOptionTwo = Radiobutton(frameaddPatientPage, text="2", variable=cptSel, value= 2)
    cptOptionTwo.pack()
    cptOptionThree = Radiobutton(frameaddPatientPage, text="3", variable=cptSel, value= 3)
    cptOptionThree.pack()


    bpsSel = IntVar(frameaddPatientPage)
    bpsScale = Scale(frameaddPatientPage, from_= 40, to=200, showvalue=True, label= "resting BPS", variable=bpsSel, orient="horizontal")
    bpsScale.pack()

    nextButton = Button(frameaddPatientPage, text="Next", fg='blue', command=lambda: addPatientPageTwo(usr, entryPatient.get(),ageSP.get(), sexSel.get(), cptSel.get(), bpsSel.get() ))
    nextButton.pack()


def addPatientPageTwo(doctor, patient, age, sex, cpt, rbp):
    if sex == "Male":
        sex = 1
    else: 
        sex = 0
    patientHealthList= [doctor, patient, int(age), int(sex), int(cpt), int(rbp)]
    clearPage()
    frameaddPatientPageTwo = Frame(frameMain)
    frameaddPatientPageTwo.pack(fill="both", expand=True)

    cholSel = IntVar(frameaddPatientPageTwo)
    cholScale = Scale(frameaddPatientPageTwo, from_= 0, to=250, showvalue=True, label= "cholesterol level", variable=cholSel, orient="horizontal")
    cholScale.pack()

    fbpsSel = StringVar(frameaddPatientPageTwo)
    fbpsPatient = Label(frameaddPatientPageTwo, text="fbps:")
    fbpsPatient.pack()
    fbsOptionZero = Radiobutton(frameaddPatientPageTwo, text="0", variable=fbpsSel, value= 0)
    fbsOptionZero.pack()
    fbsOptionOne = Radiobutton(frameaddPatientPageTwo, text="1", variable=fbpsSel, value= 1)
    fbsOptionOne.pack()

    restecgSel = StringVar(frameaddPatientPageTwo)
    restecgPatient = Label(frameaddPatientPageTwo, text="rest ecg:")
    restecgPatient.pack()
    restecgOptionZero = Radiobutton(frameaddPatientPageTwo, text="0", variable=restecgSel, value= 0)
    restecgOptionZero.pack()
    restecgOptionOne = Radiobutton(frameaddPatientPageTwo, text="1", variable=restecgSel, value= 1)
    restecgOptionOne.pack()
    restecgOptionTwo = Radiobutton(frameaddPatientPageTwo, text="2", variable=restecgSel, value= 2)
    restecgOptionTwo.pack()

    thalachSel = IntVar(frameaddPatientPageTwo)
    thalachScale = Scale(frameaddPatientPageTwo, from_= 40, to=250, showvalue=True, label= "Maximum heart rate achieved", variable=thalachSel, orient="horizontal")
    thalachScale.pack()

    exangSel = StringVar(frameaddPatientPageTwo)
    exangLabel = Label(frameaddPatientPageTwo, text="excercise induced angia:")
    exangLabel.pack()
    exangOptionOne = Radiobutton(frameaddPatientPageTwo, text="Yes", variable=exangSel, value= 1)
    exangOptionOne.pack()
    exangOptionZero = Radiobutton(frameaddPatientPageTwo, text="No", variable=exangSel, value= 0)
    exangOptionZero.pack()

    nextButton = Button(frameaddPatientPageTwo, text="Next", fg='blue', command=lambda: addPatientPageThree(patientHealthList,cholSel.get(), fbpsSel.get(), restecgSel.get(), thalachSel.get(), exangSel.get() ))
    nextButton.pack()

def addPatientPageThree(patientHealthList, chol,fbs,restecg,thalach,exang):
    patientHealthList.extend([int(chol),int(fbs),int(restecg),int(thalach),int(exang)])
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

def diagnosePatient(patientHealthList, oldpeak, slope, ca, thal):
    patientHealthList.extend([float(oldpeak), int(slope), int(ca), int(thal)])
    patientHealthList.append(neuralNetworks(patientHealthList))
    addPatient(patientHealthList)

def changePatientPage(usr):
    clearPage()
    framechangePatient = Frame(frameMain)
    framechangePatient.pack(fill="both", expand=True)

    patientSel = StringVar(framechangePatient)
    patientSel.set("Patient: ")
    patientList = []
    for item in collectPatients(usr):
        patientList.append(item[0])
    if not patientList:
        errorLabel = Label(framechangePatient, text="You have no patients to change")
        errorLabel.pack()
    else:
        patientSel = StringVar(framechangePatient)
        patientSel.set("Patient: ")
        patientMenu = OptionMenu(framechangePatient, patientSel,*patientList, command=lambda x: displayInfo(framechangePatient,patientSel.get()))
        patientMenu.pack()
        patientDisplay=Label(framechangePatient, font="Calibri,12,bold")
        patientDisplay.pack(padx=20, pady=20)

def displayInfo(frame,patientSel):
    with open("patientDatabase.csv", 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row[1] == patientSel:
                infoList = row[2:]
                for item in infoList:
                    button = Button(frame)


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

    features = np.array([[list[2], list[3], list[4], list[5], list[6], list[7], list[8], list[9], list[10], list[10], list[11], list[13], list[12]]])
    prediction = nn.predict(features)
    prediction = prediction[0]
    if prediction == 0:
        prediction = 'No'
    else:
        prediction = 'Yes'
    return prediction

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