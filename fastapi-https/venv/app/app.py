import streamlit as st
import pickle
import requests

st.title("Movie Recommender")
userid=st.text_input('Enter Userid')
option=st.selectbox('User',('New User','Returning User'))
print(userid)
print(option)

if st.button('Submit'):
    if (option=='New User'):
        st.write("New User movie list")
        res=requests.get(f"http://localhost:8432/newuser")
        st.write(res.json())
    if option=='Returning User':
        st.write(userid,"Returning User Movie List")
        res=requests.get(f"http://localhost:8432/returninguser")
        st.write(res.json())

res=requests.get(f"http://localhost:8432/docs")

st.write(res)

