import streamlit as st

page= """
<style>
</style>
"""

st.markdown(page,unsafe_allow_html=True)
st.title("Medical Assistant")
st.write("Transforming Healthcare: Recommendations That Fit Your Life")

image = st.image('../Assets/doctors.jpg')

