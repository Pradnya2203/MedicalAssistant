import streamlit as st

st.title("About Us")
st.write("Here is your comprehensive and affordable healthcare companion. Our app offers a state-of-the-art healthcare recommendation system that connects you with doctors immediately based on their availability and specialization. Whether you're in need of urgent care or planning ahead, Health Guardian allows you to book appointments at your specified location, ensuring convenience and peace of mind.")
st.markdown('''##### We are present in all these USA cities currently''')
image = st.image('../Assets/map.png')

st.markdown('''##### Feedback Form''')
feedback_message = st.text_area('Please give your feedback to help us serve you better')
rating = st.radio('Rate your experience:', ['1', '2', '3', '4', '5'])

if st.button('Submit Feedback'):
    # Save feedback to a file or database
    with open('feedback.txt', 'a') as f:
        f.write(f'Rating: {rating}, Feedback: {feedback_message}\n')
    st.success('Thank you for your feedback!')