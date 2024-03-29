import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

df=pd.read_csv("football dataset.csv")
st.title("Working with Streamlit and Football")
st.header("Data Set")
st.write(df)
with st.sidebar:
    st.title("Football Data")
    st.header("Analysis")
    st.image("football pic.png")

#WRANGLING (DATA CLEANING) BEING DONE

df_cleaned = df.dropna(subset=['Nationality', 'Position', 'Age'])
df_cleaned['Jersey Number'].fillna(np.random.randint(11, 100), inplace=True)
null_counts = df_cleaned.isnull().sum()
df = df_cleaned
st.write(df)