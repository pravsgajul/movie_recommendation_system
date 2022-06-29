import streamlit as st
import pickle
import requests
import pandas as pd

st.title("Movie Recommender")
st.write('Write 0 as userid if you are a new user.')
userid=st.text_input('Enter Userid')
option=st.selectbox('User',('New User','Returning User'))
title=st.text_input('Enter Title for Returning User')
print(userid)
print(option)

if st.button('Submit'):
    if (option=='New User'):
        st.write("New User movie list")
        res=requests.get(f"http://localhost:8432/newuser")
        newoutput=res.json()
        st.write(newoutput)

    if option=='Returning User':
        
        st.write(userid,"Returning User Movie List")
        returningres=requests.get(f"http://localhost:8432/returninguser/"+title)
        st.write(returningres.json())

res=requests.get(f"http://localhost:8432/docs")

st.write(res)

