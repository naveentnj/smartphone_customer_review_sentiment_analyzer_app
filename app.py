import streamlit as st
st.set_page_config(
    page_title="Customer_Review_Sentiment_Analyser_app",
    page_icon="👋",
    layout="wide"
)

import pandas as pd
from PIL import Image
import plotly.graph_objects as go
from plotly.subplots import make_subplots


df = pd.read_csv(r"artifacts\data_final\customer_review_with_rating_and_polarity_of_segments.csv")


def get_pos_neg_neutral(df, segment):
        positive = df[segment].value_counts()[1]
        negative = df[segment].value_counts()[2]
        neutral = df[segment].value_counts()[3]
        total = positive + negative + neutral
        return positive, negative, neutral, total

def get_percent(pos, neg, neu, total):
        pos_percent = pos / total
        neg_percent = neg / total
        neu_percent = neu / total
        return pos_percent, neg_percent, neu_percent

phone_names = df["Product Name"].unique()
st.write(tuple(phone_names))
option = st.selectbox(label="Select the phone details you need",
        options = tuple(phone_names),
        placeholder="Select phone method...")

st.write('You selected:', option)
phone_image = Image.open(f'images\{option}.jpg')

st.image(image = phone_image, width = 300)


camera_df = df[(df["Product Name"] == option) ]
performance_df = df[(df["Product Name"] == option)]
battery_df = df[(df["Product Name"] == option)]
display_df = df[(df["Product Name"] == option)]
value_for_money_df = df[(df["Product Name"] == option)]

camera_positive, camera_negative, camera_neutral,camera_total = get_pos_neg_neutral(camera_df, segment = "camera_sentiment")
performance_positive, performance_negative, performance_neutral,performance_total = get_pos_neg_neutral(performance_df,segment = "performance_sentiment")
battery_positive, battery_negative, battery_neutral,battery_total = get_pos_neg_neutral(battery_df,segment = "battery_sentiment")
display_positive, display_negative, display_neutral,display_total = get_pos_neg_neutral(display_df,segment = "display_sentiment")
value_for_money_positive, value_for_money_negative, value_for_money_neutral,value_for_money_total = get_pos_neg_neutral(value_for_money_df,segment = "value_for_money_sentiment")
overall_positive, overall_negative, overall_neutral,overall_total = get_pos_neg_neutral(value_for_money_df,segment = "overall")

# Unpack values
positive_value_camera, negative_value_camera, neutral_value_camera = get_percent(camera_positive, camera_negative, camera_neutral, camera_total)
positive_value_performance, negative_value_performance, neutral_value_performance = get_percent(performance_positive, performance_negative, performance_neutral,performance_total)
positive_value_battery, negative_value_battery, neutral_value_battery = get_percent(battery_positive, battery_negative, battery_neutral,battery_total)
positive_value_display, negative_value_display, neutral_value_display = get_percent(display_positive, display_negative, display_neutral,display_total)
positive_value_value_for_money, negative_value_value_for_money, neutral_value_value_for_money = get_percent(value_for_money_positive, value_for_money_negative, value_for_money_neutral,value_for_money_total)
positive_value_overall, negative_value_overall, neutral_value_overall = get_percent(overall_positive, value_for_money_negative, value_for_money_neutral,value_for_money_total)


st.markdown(f"""## Rating {df["rating_num"].mean()}""")
st.markdown(f"""## Camera, Performance, Battery, \n ## Display, Value for Money, Overall """)

labels = ["positive", "negative","neutral"]
fig = make_subplots(rows=2, cols=3, specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}],[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]])
fig.add_trace(go.Pie(labels=labels, values=[positive_value_camera,negative_value_camera,neutral_value_camera], name="Camera"),1, 1)
fig.add_trace(go.Pie(labels=labels, values=[positive_value_performance,negative_value_performance,neutral_value_performance], name="Performance"),1, 2)
fig.add_trace(go.Pie(labels=labels, values=[positive_value_battery,negative_value_battery,neutral_value_battery], name="battery"),1, 3)
fig.add_trace(go.Pie(labels=labels, values=[positive_value_display,negative_value_display,neutral_value_display], name="Performance"),2, 1)
fig.add_trace(go.Pie(labels=labels, values=[positive_value_value_for_money,negative_value_value_for_money,neutral_value_value_for_money], name="value_for_money"),2, 2)
fig.add_trace(go.Pie(labels=labels, values=[positive_value_overall,negative_value_overall,neutral_value_overall], name="overall"),2, 3)

# Use `hole` to create a donut-like pie chart
fig.update_traces(hole=.4)

fig.update_layout(
    title_text="Positive Negative for performance and camera",
    # Add annotations in the center of the donut pies.
    annotations=[dict(text='', x=0.18, y=0.5, font_size=10, showarrow=False),
                 dict(text='', x=0.82, y=0.5, font_size=10, showarrow=False),
                 dict(text='', x=0.82, y=0.5, font_size=10, showarrow=False),
                 dict(text='', x=1.18, y=0.5, font_size=10, showarrow=False),
                 dict(text='', x=1.5, y=0.5, font_size=10, showarrow=False)])
fig.update_layout(
    autosize=False,
    width=400,
    height=400,
    margin=dict(
        l=50,
        r=50,
        b=100,
        t=100,
        pad=4
    ),
)

st.plotly_chart(fig, theme="streamlit", use_container_width=False)


