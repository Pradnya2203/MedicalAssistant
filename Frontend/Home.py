import streamlit as st

st.title("Health Guardian")
st.write("Transforming Healthcare: Recommendations That Fit Your Life")

image = st.image('../Assets/doctor.png',width=500)

st.page_link("pages/Connect_Now.py", label="Connect Now",icon="1️⃣")
st.caption("To have an immediate video call or chat with one of our experts, Head on to the Contact Now Page")
st.page_link("pages/Schedule_Appointment.py", label="Schedule Appointment",icon="2️⃣")
st.caption("To book an in-person appointment, Head on to our Schedule Appointment Page")
st.page_link("pages/Test_Yourself.py", label="Test Yourself",icon="3️⃣")
st.caption("To have a quick test yourself, Head on to our Test Yourself Page")
st.page_link("pages/About_Us.py", label="About Us", icon="🌎")
st.caption("To know more about us, Head on to the About Us page and do leave a feedback there")


