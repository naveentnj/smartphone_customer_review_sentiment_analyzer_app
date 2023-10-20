import pandas as pd
import numpy as np
import demoji
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax
import googletrans
from tqdm import tqdm
import torch.nn.functional as F
import torch

MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

# Download emoji data
#demoji.download_codes()
translator = googletrans.Translator()

def remove_emojis(text):
    return demoji.replace_with_desc(str(text), sep=' ')


def translate_review(text, dest='en'):
    text = str(text)
    try:
        translation = translator.translate(text, dest=dest)
        return translation.text
    except AttributeError:
        print('Error retrieving translation token. Please try again later.')
    return None

def detect_lang_run(input_text):
    detected = translator.detect(input_text)
    count = 0
    if detected.lang != "en":

        if isinstance(detected.confidence, list) and detected.confidence[0] < 1:
            input_text = translate_review(input_text)
            count += 1
    return input_text

def polarity_score_roberta(example):
    try:
        encoded_text = tokenizer(example, return_tensors='pt', truncation=True, max_length=514)
        output = model(**encoded_text)
        scores = output[0][0].detach().numpy()
        scores = torch.as_tensor(scores)
        scores = softmax(scores)
        scores = scores.view(-1)
        sentiment = torch.argmax(scores)
        # Convert the argmax value to a polarity score of 1, 2, or 3.
        if sentiment == 0:
            return 3  # Negative
        elif sentiment == 1:
            return 2  # Neutral
        else:
            return 1  # Positive
    except IndexError:
        # Handle index out of range error
        return 2  # Neutral as a default value
    except Exception as e:
        # Handle other runtime errors
        print(f"Error: {e}")
        return 0  # Return 0 or handle it according to your specific case
    
def set_polarity(tweet):
    flag = 0 
    if isinstance(tweet, str):
        flag = polarity_score_roberta(tweet)
    return flag

def identify_subject_set_polarity(tweet, refs):
    flag = 0 
    for ref in refs:
        if isinstance(tweet, str) and tweet.find(ref) != -1:
            tweet_split = tweet.split(".")
            for sentence in tweet_split:
                if isinstance(sentence, str) and sentence.find(ref) != -1:
                    flag = polarity_score_roberta(sentence)
    return flag

def data_transform(df):
    df = df.drop(df.columns[0], axis=1)

    df.insert(0, 'Id', range(1, 1 + len(df)))
    
    tqdm.pandas()
    # Apply the function to the 'Review-Body' column
    df['Review-Body'] = df['Review-Body'].apply(remove_emojis)

    
    remove_newspace = lambda x: ' '.join(x.replace('\n', ' ').split())
    # Apply the lambda function to the "Review" column
    df["Review-Body"] = df["Review-Body"].apply(remove_newspace)

    tqdm.pandas()
    df['Review-Body'] = df['Review-Body'].progress_apply(detect_lang_run)

    battery = ['Battery', 'Charge', 'charging']
    performance = ['Performance', 'Speed']
    display = ["display", "screen", "brightness"]
    camera = ["camera","megapixel","images","capture"]
    value_for_money = ["good","price","money","value for money"]

    tqdm.pandas()
    df['battery_sentiment'] = df['Review-Body'].progress_apply(lambda x: identify_subject_set_polarity(x, battery)) 
    df['performance_sentiment'] = df['Review-Body'].progress_apply(lambda x: identify_subject_set_polarity(x, performance))
    df['display_sentiment'] = df['Review-Body'].progress_apply(lambda x: identify_subject_set_polarity(x, display))
    df['camera_sentiment'] = df['Review-Body'].progress_apply(lambda x: identify_subject_set_polarity(x, camera))
    df['value_for_money_sentiment'] = df['Review-Body'].progress_apply(lambda x: identify_subject_set_polarity(x, value_for_money))
    df['overall'] = df['Review-Body'].progress_apply(lambda x: set_polarity(x))

    # Save the final CSV
    print("done")
    df.to_csv("artifacts\data_transformation_new\new\customer_review_with_rating_and_polarity.csv")
    return df

