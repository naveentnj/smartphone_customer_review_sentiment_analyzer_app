import streamlit as st
import pandas as pd
from textSentimentAnalyser.pipeline.stage_02_data_transform import data_transform

df = pd.read_csv("artifacts\data_ingestion\mobile_phone_data.csv")
#input_file = st.file_uploader(label = "Upload the CSV Review Data")

#df = pd.read_csv(input_file)

df = data_transform(df)
phone_names = df["Product Name"].unique()
st.write(tuple(phone_names))
#for i in phone_names:
#    print(type(i))
option = st.selectbox(label="Select the phone details you need",
        options = tuple(phone_names),
        placeholder="Select contact method...")

st.write('You selected:', option)

battery_df = df[(df["Product Name"] == option) & (df['battery'] == 1)]
battery_neg_avg = battery_df['neg'].mean()
battery_pos_avg = battery_df['pos'].mean()
battery_rating_avg = battery_df['rating_num'].mean()

st.write("Battery positive of " , option , " is ", (battery_pos_avg * 100))
st.write("Battery rating of " , option , " is ", battery_rating_avg)