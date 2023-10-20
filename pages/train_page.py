import streamlit as st
import pandas as pd
from PIL import Image
from textSentimentAnalyser.pipeline.stage_02_data_transform import data_transform

existing_db = pd.read_csv("artifacts\data_final\customer_review_with_rating_and_polarity_of_segments.csv")
input_file = st.file_uploader(label = "Upload the CSV Review Data")

df = pd.read_csv(input_file)
result_df =  data_transform(df)
appended_df = result_df.append(existing_db, ignore_index=True)