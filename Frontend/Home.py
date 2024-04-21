import streamlit as st



# if st.button('Call Ambulance',button_color='red'):
#     st.markdown('[Click here to call] (tel:100)')

page= """
<style>
</style>
"""

st.markdown(page,unsafe_allow_html=True)
st.title("Health Guardian")
st.write("Transforming Healthcare: Recommendations That Fit Your Life")

image = st.image('../Assets/doctors.jpg',width=500)

st.page_link("pages/Connect_Now.py", label="Connect Now",icon="1️⃣")
st.caption("To have an immediate video call or chat with one of our experts, Head on to the Contact Now Page")
st.page_link("pages/Schedule_Appointment.py", label="Schedule Appointment",icon="2️⃣")
st.caption("To book an in-person appointment, Head on to our Schedule Appointment Page")
st.page_link("pages/About_Us.py", label="About Us", icon="🌎")
st.caption("To know more about us, Head on to the About Us page and do leave a feedback there")


