import streamlit as st
import matplotlib.pyplot as plt
import joblib
import pandas as pd
import seaborn as sns
from sklearn.metrics import accuracy_score, precision_score

# add title to streamlit webapp
st.title('Monitoring Dashboard')

# create pandas dataframe from the logs file and add num_words column
def load_logs(file_path):
    df = pd.read_json(file_path, lines=True)


    df['num_words'] = df['request_text'].apply(lambda x: len(x.split()))
    return(df)

# create pandas dataframe from the IMDB dataset and add num_words column
def load_existing_data(file_path):
    df = pd.read_csv(file_path)
    df['num_words'] = df['review'].apply(lambda x: len(x.split()))

    return(df)

# create dataframes
logs_df = load_logs('../logs/prediction_logs.ndjson')
data_df = load_existing_data('IMDB_Dataset.csv')

# Display Accuracy
accuracy = accuracy_score(logs_df["true_label"], logs_df["predicted_label"])
st.text(f'Model Accuracy: {accuracy}')

if accuracy < .80:
    st.error("Model Accuracy Has Fallen Below 80%")

# Display Precision
precision = precision_score(logs_df["true_label"], logs_df["predicted_label"], pos_label='positive')
st.text(f'Model Precision: {precision}')

# first plots
fig, axes = plt.subplots(1,2, figsize=(12,5))
sns.kdeplot(data=logs_df, x = 'num_words', ax=axes[0])
sns.kdeplot(data=data_df, x = 'num_words', ax=axes[1], color="orange")

axes[0].set_title('Logged Sentence Lengths')
axes[1].set_title('IMDB Data Sentence Length')

axes[0].set_xlabel("Number of Words")
axes[1].set_xlabel("Number of Words")

st.pyplot(fig)

# second plots
fig, axes = plt.subplots(1,2, figsize=(12,5))
sns.histplot(data=logs_df, x = 'predicted_label', ax=axes[0], hue='predicted_label')
sns.histplot(data=data_df, x = 'sentiment', ax=axes[1], hue='sentiment')

axes[0].set_title('Predicted Labels')
axes[1].set_title('IMDB Data Labels')

axes[0].set_xlabel("Labels")
axes[1].set_xlabel("Labels")

st.pyplot(fig)



