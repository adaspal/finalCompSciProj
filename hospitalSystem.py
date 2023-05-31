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

import csv

def neuralNetworks(list): 
    data = pd.read_csv('./dataset/heart.csv')

    # Split train data
    y=data.target
    x=data.drop('target',axis=1)

    sample_train, sample_val, labels_train, labels_val = train_test_split(x,y,test_size=0.35, random_state=42)

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

    features = np.array([[list[0], list[1], list[2], list[3], list[4], list[5], list[6], list[7], list[8], list[9], list[10], list[11], list[12]]])
    prediction = nn.predict(features)
    print("Prediction: ", prediction)

# Main Code
win = Tk()
win.title("Hospital System")
win.geometry("700x500")
age = int(input("Age: "))
sex = int(input("Sex: "))
cp = int(input("Chest Pain Type 1-4: "))
rbp = int(input("Resting Blood Pressure: "))
chol = int(input("Serum Cholestoral: "))
fbs = int(input("Fasting Blood Sugar: "))
rer = int(input("Resting Electrocardiographic Results 0-2: "))
hr = int(input("Max. Heart Rate: "))
eia = int(input("exercise induced angina: "))
oldpeak = float(input("ST depression induced by exercise: "))
slope = int(input("Slope of peak: "))
ves = int(input("Vessel # colored by flouroscopy "))
thal = int(input("Thal 0-2: "))
myList = [age, sex, cp, rbp, chol, fbs, rer, hr, eia, oldpeak, slope, ves, thal]
neuralNetworks(myList)

# Doesn't allow the screen to be resized
win.resizable(0, 0)

frameMain = Frame(win) #All other created frames are children of this frame, making them contained under frameMain
frameMain.pack(expand=True, anchor="n") 

# loginpage()

win.mainloop()