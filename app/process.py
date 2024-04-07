import pandas as pd
import tensorflow_hub as hub
import tensorflow_text
import tensorflow as tf
import numpy as np
import json
import re

# Load the Universal Sentence Encoder
use_model = hub.load("https://tfhub.dev/google/universal-sentence-encoder-multilingual/3")

# Read the CSV file
data = pd.read_csv('training/College_previous_projects.csv')


# Function to clean text
def clean_text(text):
    # Remove non-alphanumeric characters and symbols
    cleaned_text = re.sub(r'[^\w\s]', '', text)
    return cleaned_text

# Function to compute cosine similarity
def cosine_similarity(a, b):
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return dot_product / (norm_a * norm_b)

def find_matches(user_title, user_abstract, user_algorithm, user_methodology):
    matched_list = []
    # Preprocess the data
    data['Abstract'] = data['Abstract'].apply(clean_text)
    data['Algorithm'] = data['Algorithm'].apply(clean_text)
    data['Methodology'] = data['Methodology'].apply(clean_text)

    for index, row in data.iterrows():
        # Extract Title, Abstract, Algorithm, and Methodology for each row
        title = row['Title']
        abstract = row['Abstract']
        algorithm = row['Algorithm']
        methodology = row['Methodology']

        # Calculate embeddings for the strings
        embedding1 = use_model([title])[0]
        embedding2 = use_model([abstract])[0]
        embedding3 = use_model([algorithm])[0]
        embedding4 = use_model([methodology])[0]
        embedding5 = use_model([user_title])[0]
        embedding6 = use_model([user_abstract])[0]
        embedding7 = use_model([user_algorithm])[0]
        embedding8 = use_model([user_methodology])[0]

        # Calculate cosine similarity between the embeddings
        cosine_sim_title = round(((cosine_similarity(embedding5, embedding1)) * 100) , 2)
        cosine_sim_abstract = round(((cosine_similarity(embedding6, embedding2)) * 100) , 2)
        cosine_sim_algorithm = round(((cosine_similarity(embedding7, embedding3)) * 100) , 2)
        cosine_sim_methodology = round(((cosine_similarity(embedding8, embedding4)) * 100) , 2)

        # Check if any cosine similarity is greater than 50
        if (cosine_sim_title > 60) or (cosine_sim_abstract > 60) or (cosine_sim_algorithm > 65) or (cosine_sim_methodology > 80):
            matched_list.append({"Title" : title, "Abstract" : abstract, "Algorithm" : algorithm, "Methodology" : methodology, "similarity_title" : cosine_sim_title,
                                 "similarity_abstract" : cosine_sim_abstract, "similarity_algorithm" : cosine_sim_algorithm, "similarity_methodology" : cosine_sim_methodology})
            
    return matched_list