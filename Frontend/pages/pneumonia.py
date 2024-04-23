import pandas as pd
import numpy as np
import streamlit as st
import pickle

model_path = "../Backend/diabetes.sav"
model = pickle.load(open(model_path, 'rb'))

model_path1 = "../Backend/heart_risk.sav"
model1 = pickle.load(open(model_path1, 'rb'))

def main():
    Glucose = st.number_input('Glucose',min_value=1, max_value=200,value=100,step=2)
    BMI = st.number_input('BMI',min_value=1.0, max_value=200.0,value=20.0,step=0.5)
    Age = st.number_input('Age',min_value=1, max_value=200,value=25,step=1)
    Pregnancies = st.number_input('Pregnancies',min_value=0, max_value=100,value=0,step=1)
    DiabetesPedigreeFunction = st.number_input('DiabetesPedigreeFunction',min_value=0.07, max_value=2.42,value=0.07,step=0.01)
    features = [[Glucose, BMI, Age, Pregnancies, DiabetesPedigreeFunction]]
    if st.button("Check Diabetes"):
        prediction = model.predict(features)
        prediction = prediction[0]
        if(prediction==1):
            st.write("You have a high chance of having diabetes")
        else:
             st.write("You have a low chance of having diabetes")

    age = st.number_input('age',min_value=1, max_value=200,value=25,step=1)
    Serum_cholesterol = st.number_input('Serum_cholestrol',min_value=100.0, max_value=600.0,value=200.0,step=0.01)
    X = [[age, Serum_cholesterol]]
    if st.button("Check heart risk"):
        pred = model1.predict(X)
        st.write(pred[0])




if __name__=='__main__':
    main()