import pandas as pd
import numpy as np
import streamlit as st
import pickle
from fuzzywuzzy import process
from streamlit_extras.add_vertical_space import add_vertical_space

st.markdown('''## Contact Now''')

st.caption("If you're not feeling well, reach out to a doctor right away and share your symptoms for the care you need")

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
    sorted_df_desc = filtered_df.sort_values(by='Rating', ascending=False)
    return sorted_df_desc



def main():
    st.markdown('''#### Please give your information''')
    Name = st.text_input("Enter your name:")
    st.markdown('''#### Mention your symptoms here''')
    Symptom1 = st.text_input("Symptom 1")
    Symptom2 = st.text_input("Symptom 2 (Optional)")
    Symptom3 = st.text_input("Symptom 3 (Optional)")
    Symptom4 = st.text_input("Symptom 4 (Optional)")
    Symptom5 = st.text_input("Symptom 5 (Optional)")

    
    if st.button("Check Availability"):
        data=predict_disease(Symptom1,Symptom2,Symptom3,Symptom4,Symptom5)
        data = data.reset_index()
        st.write(f"{Name}, you should consider reaching out to a {data.loc[0, 'Specialization']}")
        st.write("Here is the list of doctors available at the moment")
        avail = data[data['Availability'] == 1]
        if avail.empty:
            st.write("Sorry, none of our doctors are online at the moment")
        else:
            columns_to_drop = ['Availability', 'Monday','Tuesday','Wednestday','Thursday','Friday','Saturday','index']
            avail=avail.drop(columns=columns_to_drop)
            avail=avail.head(5)
            st.write(avail)
            st.write("You can choose to have a quick chat/video call with them right now or book an appointment later by heading to the appointment page")

    st.write("Thank You for visiting us")
if __name__=='__main__':
    main()


