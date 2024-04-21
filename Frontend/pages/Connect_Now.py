import pandas as pd
import numpy as np
import streamlit as st
import pickle
from fuzzywuzzy import process
from streamlit_extras.add_vertical_space import add_vertical_space

st.markdown('''## Contact Now''')

st.caption("Book an online appointment with a doctor here! If you're unsure of what kind of doctor you should consult, list down your symptoms, and we'll do the work for you")

model_path = "../Backend/rnd_forest.sav"
model = pickle.load(open(model_path, 'rb'))

list_of_symptoms = pd.read_csv("../Backend/Dataset/list_of_symptoms.csv")
symptoms = list_of_symptoms['Symptoms'].to_list()

symptoms_severity = pd.read_csv("../Backend/Dataset/Symptom-severity.csv")
symptoms_severity['Symptom'] = symptoms_severity['Symptom'].str.replace('_',' ')

disease_specialization = pd.read_csv("../Backend/Dataset/disease-specialization.csv")

doc_data = pd.read_csv("../Backend/Dataset/doc-data.csv")

data = pd.DataFrame()

def predict_disease(Symptom1,Symptom2,Symptom3,Symptom4,Symptom5):


    array = [0 for _ in range(17)]
    # for i in range(len(symptoms)):
    if Symptom1.strip():
        closest_match, score = process.extractOne(Symptom1, symptoms)
        array[0] = symptoms_severity[symptoms_severity['Symptom'] == closest_match]['weight'].values[0]
    if Symptom2.strip():
        closest_match, score = process.extractOne(Symptom2, symptoms)
        array[1] = symptoms_severity[symptoms_severity['Symptom'] == closest_match]['weight'].values[0]
    if Symptom3.strip():
        closest_match, score = process.extractOne(Symptom3, symptoms)
        array[2] = symptoms_severity[symptoms_severity['Symptom'] == closest_match]['weight'].values[0]
    if Symptom4.strip():
        closest_match, score = process.extractOne(Symptom4, symptoms)
        array[3] = symptoms_severity[symptoms_severity['Symptom'] == closest_match]['weight'].values[0]
    if Symptom5.strip():
        closest_match, score = process.extractOne(Symptom5, symptoms)
        array[4] = symptoms_severity[symptoms_severity['Symptom'] == closest_match]['weight'].values[0]

    array = np.array(array)
    array=array.reshape(1, -1)
    prediction = model.predict(array)
    st.write(f"It looks like you may have {prediction[0]}")
    result = disease_specialization[disease_specialization['Disease']==prediction[0]]['Specialization'].values[0]
    filtered_df = doc_data[doc_data['Specialization'] == result]
    sorted_df_desc = filtered_df.sort_values(by='User Rating', ascending=False)
    return sorted_df_desc



def main():
    st.markdown('''#### Please give your information''')
    Name = st.text_input("Enter your name:")

    st.markdown('''##### Search based on the specilization of the doctor''')
    question = "Choose the specialization of the doctor"
    specializations = ['Dermatologist', 'Endocrinologist', 'Infectious Disease Specialist', 'Gastroenterologist', 'Cardiologist', 'Rheumatologist', 'Neurologist', 'Urologist', 'Proctologist', 'Orthopedic Surgeon', 'Pulmonologist', 'Allergist/Immunologist', 'Vascular Surgeon', 'Pharmacologist', 'Ear, Nose, and Throat (ENT) Specialist', 'General Practitioner (GP)'] 
    answer = st.selectbox(question, specializations)

    if st.button("Check Availability"):
        data = doc_data[doc_data['Specialization'] == answer]
        data = data[data['Availability'] == 1]
        if data.empty:
            st.write(f"Sorry {Name}, no {answer} are available at the moment")
        else:
            columns_to_drop = ['Availability', 'Monday','Tuesday','Wednestday','Thursday','Friday','Saturday']
            data = data.drop(columns=columns_to_drop)
            sorted_df = data.sort_values(by='User Rating', ascending=False)
            sorted_df=sorted_df.head(5)
            st.write(f"The following {answer} are online right now, you can choose to have a chat or video call session with them")
            st.write(sorted_df)


    st.markdown('''##### If you are unsure about which doctor to consult, we can help you with that''')
    st.markdown('''##### Please mention your symptoms here''')
    Symptom1 = st.text_input("Symptom 1")
    Symptom2 = st.text_input("Symptom 2 (Optional)")
    Symptom3 = st.text_input("Symptom 3 (Optional)")
    Symptom4 = st.text_input("Symptom 4 (Optional)")
    Symptom5 = st.text_input("Symptom 5 (Optional)")

    
    if st.button("Analyze Symptoms"):
        data=predict_disease(Symptom1,Symptom2,Symptom3,Symptom4,Symptom5)
        data = data.reset_index()
        st.write(f"{Name}, you should consider reaching out to a {data.loc[0, 'Specialization']}")
        st.write("Here is the list of doctors available at the moment")
        avail = data[data['Availability'] == 1]
        if avail.empty:
            st.write(f"Sorry {Name}, none of our doctors are online at the moment")
        else:
            columns_to_drop = ['Availability', 'Monday','Tuesday','Wednestday','Thursday','Friday','Saturday','index']
            avail=avail.drop(columns=columns_to_drop)
            avail=avail.head(5)
            st.write(f"The following {answer} are online right now, you can choose to have a chat or video call session with them")
            st.write(avail)
            st.write("If you want to have an in-person appointment, Head on to our Schedule Appointment page")
    st.write("Thank You for visiting us")
if __name__=='__main__':
    main()



