import pandas as pd
import numpy as np
import demoji
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax
import googletrans

# Download emoji data
demoji.download_codes()


def remove_emojis(text):
    return demoji.replace_with_desc(str(text), sep=' ')

def translate_review(text, dest='en'):
    text = str(text)
    translator = googletrans.Translator()
    try:
        translation = translator.translate(text, dest=dest)
        return translation.text
    except AttributeError:
        print('Error retrieving translation token. Please try again later.')
        return None

    

def identify_subject(tweet, refs):
    flag = 0 
    for ref in refs:
        if isinstance(tweet, str) and tweet.find(ref) != -1:
            flag = 1
    return flag

def data_transform(df):
    df = df.drop(df.columns[0], axis=1)

    df.insert(0, 'Id', range(1, 1 + len(df)))

    # Apply the function to the 'Review-Body' column
    df['Review-Body'] = df['Review-Body'].apply(remove_emojis)

    df['Review-Body'] = df['Review-Body'].apply(translate_review)

    battery = ['Battery', 'Charge', 'charging']
    performance = ['Performance', 'Speed']
    display = ["display", "screen", "brightness"]
    camera = ["camera","megapixel","images","capture"]

    df['battery'] = df['Review-Body'].apply(lambda x: identify_subject(x, battery)) 
    df['performance'] = df['Review-Body'].apply(lambda x: identify_subject(x, performance))
    df['display'] = df['Review-Body'].apply(lambda x: identify_subject(x, display))
    df['camera'] = df['Review-Body'].apply(lambda x: identify_subject(x, camera))

    # Save the final CSV
    df.to_csv("artifacts\data_transformation_new\customer_review_with_rating_and_polarity.csv")
    return df