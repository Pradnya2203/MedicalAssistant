import pandas as pd
import numpy as np
import streamlit as st
import pickle
from fuzzywuzzy import process
from streamlit_extras.add_vertical_space import add_vertical_space

st.markdown('''## Schedule An Appointment''')

st.caption("Book an in-person appointment with a doctor here! You can check their availability and match it with yours. If you're unsure of what kind of doctor you should consult, list down your symptoms, and we'll do the work for you ")

list_of_symptoms = pd.read_csv("../Backend/Dataset/list_of_symptoms.csv")
symptoms = list_of_symptoms['Symptoms'].to_list()

model_path = "../Backend/rnd_forest.sav"
model = pickle.load(open(model_path, 'rb'))

symptoms_severity = pd.read_csv("../Backend/Dataset/Symptom-severity.csv")
symptoms_severity['Symptom'] = symptoms_severity['Symptom'].str.replace('_',' ')

symptom_precaution = pd.read_csv("../Backend/Dataset/symptom_precaution.csv")
symptom_description = pd.read_csv("../Backend/Dataset/symptom_Description.csv")

disease_specialization = pd.read_csv("../Backend/Dataset/disease-specialization.csv")

doc_data = pd.read_csv("../Backend/Dataset/doc-data.csv")

def predict_disease(Symptom1,Symptom2,Symptom3,Symptom4,Symptom5):


    array = [0 for _ in range(17)]
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
    result = disease_specialization[disease_specialization['Disease']==prediction[0]]['Specialization'].values[0]
    st.write(f"It looks like you may have {prediction[0]}, you should consult a {result}")
    description = symptom_description[symptom_description['Disease']==prediction[0]]
    description = description['Description'].tolist()
    st.write(description[0])
    precaution = symptom_precaution[symptom_precaution['Disease']==prediction[0]]
    precaution1 = precaution['Precaution_1'].tolist()
    precaution2 = precaution['Precaution_2'].tolist()
    precaution3 = precaution['Precaution_3'].tolist()
    precaution4 = precaution['Precaution_4'].tolist()
    filtered_df = doc_data[doc_data['Specialization'] == result]
    sorted_df_desc = filtered_df.sort_values(by='User Rating', ascending=False)
    return [sorted_df_desc,precaution1[0],precaution2[0],precaution3[0],precaution4[0],prediction[0]]



def main():
    st.markdown('''#### Please give your information''')
    Name = st.text_input("Enter your name:")
    Location = st.text_input("Enter your location:")

    question = "To book an appointment , choose a day suitable to you"
    options = ['Any','Monday','Tuesday','Wednestday','Thursday','Friday','Saturday']
    answer = st.selectbox(question, options)

    st.markdown('''##### Search based on the specilization of the doctor''')
    question1 = "Choose the specialization the doctor"
    specializations = ['Dermatologist', 'Endocrinologist', 'Infectious Disease Specialist', 'Gastroenterologist', 'Cardiologist', 'Rheumatologist', 'Neurologist', 'Urologist', 'Proctologist', 'Orthopedic Surgeon', 'Pulmonologist', 'Allergist/Immunologist', 'Vascular Surgeon', 'Pharmacologist', 'Ear, Nose, and Throat (ENT) Specialist', 'General Practitioner (GP)'] 
    answer1 = st.selectbox(question1, specializations)

    if st.button("Check Schedule"):
        data = doc_data[doc_data['Specialization'] == answer1]
        if not (data['Location'] == Location).any():
            st.write("Sorry, we are not present in these locations yet, however you can use our online services")
        else:
            data = data[data['Location'] == Location]
            if data.empty:
                st.write(f"Sorry {Name}, no {answer1} are available at the moment")
            else:
                if answer == 'Any':
                    columns_to_drop = ['Availability', 'Location']
                    data = data.drop(columns=columns_to_drop)
                else:
                    data['Time Slot'] = data[answer]
                    columns_to_drop = ['Availability', 'Monday','Tuesday','Wednestday','Thursday','Friday','Saturday','Location']
                    data = data.drop(columns=columns_to_drop)
                sorted_df = data.sort_values(by='User Rating', ascending=False)
                sorted_df=sorted_df.head(5)
                st.write(f"The following {answer1} are available on your prefered day at {Location}, book an appointment soon")
                st.write(sorted_df)

    st.markdown('''##### If you are unsure about which doctor to consult, we can help you with that''')
    st.markdown('''##### Please mention your symptoms here''')
    Symptom1 = st.text_input("Symptom 1")
    Symptom2 = st.text_input("Symptom 2 (Optional)")
    Symptom3 = st.text_input("Symptom 3 (Optional)")
    Symptom4 = st.text_input("Symptom 4 (Optional)")
    Symptom5 = st.text_input("Symptom 5 (Optional)")

    

    if st.button("Analyze Symptoms"):
        output=predict_disease(Symptom1,Symptom2,Symptom3,Symptom4,Symptom5)
        data = output[0]
        data = data.reset_index()
        if answer == 'Any':
            avail = data
        else:
            avail = data[data[answer] != "None"]
        if avail.empty:
            st.write("Sorry, nothing is available at the moment, please reach out again soon")
        else:
            if not (avail['Location'] == Location).any():
                st.write("Sorry, we are not present in these locations yet, however you can use our online services")
            else:
                avail = avail[avail['Location']==Location]
                if avail.empty:
                    st.write("Sorry, nothing is available at the moment, please reach out again soon")
                else:
                    if(answer == 'Any'):
                        columns_to_drop = ['Availability','Location','index']
                        avail=avail.drop(columns=columns_to_drop)
                    else:
                        avail['Time Slot'] = avail[answer]
                        columns_to_drop = ['Availability', 'Monday','Tuesday','Wednestday','Thursday','Friday','Saturday','Location','index']
                        avail=avail.drop(columns=columns_to_drop)
                    avail=avail.head(5)
                    st.write(f"{Name}, The Doctors available on your prefered day at {Location} are:")
                    st.write(avail)
                    st.write(f"If you want to have an immediate video call or chat with one of our doctors, Head on to Contact Now page")

                    st.markdown('''##### Few preventive measures you can try for relief''')
                    for i in range(4):
                        st.markdown("- " +output[i+1])
    st.markdown('''###### Thank You for visiting us''')
if __name__=='__main__':
    main()



