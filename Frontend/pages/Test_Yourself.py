import pandas as pd
import numpy as np
import streamlit as st
import pickle

model_path_diabetes = "../Backend/diabetes.sav"
diabetes_pred = pickle.load(open(model_path_diabetes, 'rb'))

model_path_heart_risk = "../Backend/heart_risk.sav"
heart_risk_pred = pickle.load(open(model_path_heart_risk, 'rb'))

def main():
    st.subheader("Diabetes")
    st.write("Diabetes is a chronic condition that affects how your body turns food into energy. There are two main types of diabetes")
    Glucose = st.number_input('Glucose',min_value=1, max_value=200,value=100,step=2)
    BMI = st.number_input('BMI',min_value=1.0, max_value=200.0,value=20.0,step=0.5)
    Age = st.number_input('Age',min_value=1, max_value=200,value=25,step=1)
    Pregnancies = st.number_input('Number of Pregnancies',min_value=0, max_value=100,value=0,step=1)
    DiabetesPedigreeFunction = st.number_input('Diabetes Pedigree Function',min_value=0.07, max_value=2.42,value=0.07,step=0.01)
    features = [[Glucose, BMI, Age, Pregnancies, DiabetesPedigreeFunction]]
    if st.button("Check Diabetes"):
        prediction = diabetes_pred.predict(features)
        if(prediction[0]==1):
            st.write("You have a high chance of having diabetes")
        else:
             st.write("You have a low chance of having diabetes")

    st.subheader("Risk for Heart Diseases")
    st.write("High serum cholesterol levels are associated with an increased risk of developing atherosclerosis leading to complications such as coronary artery disease, heart attack, or stroke. High cholesterol levels are a major risk factor for atherosclerosis and heart disease.")
    age = st.number_input('age',min_value=1, max_value=200,value=25,step=1)
    Serum_cholesterol = st.number_input('Serum Cholestrol Levels',min_value=100.0, max_value=600.0,value=200.0,step=0.01)
    X = [[age, Serum_cholesterol]]
    if st.button("Check heart risk"):
        pred = heart_risk_pred.predict(X)
        st.write(pred[0])
        if(pred[0]==1):
            st.write("You have a high heart risk")
        else:
            st.write("You have a low heart risk")




if __name__=='__main__':
    main()