import pandas as pd
import numpy as np
import streamlit as st
import pickle
from fuzzywuzzy import process
from streamlit_extras.add_vertical_space import add_vertical_space

st.markdown('''## Schedule An Appointment''')

st.caption("Schedule an appointment here")

list_of_symptoms = pd.read_csv("../Backend/Dataset/list_of_symptoms.csv")
symptoms = list_of_symptoms['Symptoms'].to_list()

model_path = "../Backend/rnd_forest.sav"
model = pickle.load(open(model_path, 'rb'))

symptoms_severity = pd.read_csv("../Backend/Dataset/Symptom-severity.csv")
symptoms_severity['Symptom'] = symptoms_severity['Symptom'].str.replace('_',' ')

disease_specialization = pd.read_csv("../Backend/Dataset/disease-specialization.csv")

doc_data = pd.read_csv("../Backend/Dataset/doc-data.csv")

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
    result = disease_specialization[disease_specialization['Disease']==prediction[0]]['Specialization'].values[0]
    st.write(f"It looks like you may have {prediction[0]}")
    filtered_df = doc_data[doc_data['Specialization'] == result]
    sorted_df_desc = filtered_df.sort_values(by='Rating', ascending=False)
    return sorted_df_desc



def main():
    st.markdown('''#### Please give your information''')
    Name = st.text_input("Enter your name:")
    Location = st.text_input("Enter your location:")
    st.markdown('''#### Mention your symptoms here''')
    Symptom1 = st.text_input("Symptom 1")
    Symptom2 = st.text_input("Symptom 2 (Optional)")
    Symptom3 = st.text_input("Symptom 3 (Optional)")
    Symptom4 = st.text_input("Symptom 4 (Optional)")
    Symptom5 = st.text_input("Symptom 5 (Optional)")

    st.write("If you want to book an appointment tomorrow, choose a convinient time for you")
    question = "When do you want to book an appointment"
    options = ['Monday','Tuesday','Wednestday','Thursday','Friday','Saturday']
    answer = st.selectbox(question, options)

    if st.button("Schedule"):
        data=predict_disease(Symptom1,Symptom2,Symptom3,Symptom4,Symptom5)
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
                    avail['Time Slot'] = avail[answer]
                    columns_to_drop = ['Availability', 'Monday','Tuesday','Wednestday','Thursday','Friday','Saturday','Location']
                    avail=avail.drop(columns=columns_to_drop)
                    avail=avail.head(5)
                    st.write(f"{Name}, The Doctors available on {answer} at {Location} are:")
                    st.write(avail)
                    avail = avail.reset_index()
                    st.write(f"You can book an appointment on {answer} at the available time in {Location}, or you can also have a quick video call or chat with one of our experts online by heading to the immediate page")

    st.write("Thank You for visiting us")
if __name__=='__main__':
    main()


