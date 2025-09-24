# ml_models/chatbot/final_predict.py (Corrected Version)

import json
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
import pickle
import random
import os

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# --- Load the saved model and other necessary files ---
dir_path = os.path.dirname(os.path.realpath(__file__))
model_path = os.path.join(dir_path, "chatbot_model.pkl")
lbl_encoder_path = os.path.join(dir_path, "label_encoder.pkl")
all_words_path = os.path.join(dir_path, "all_words.pkl")
intents_path = os.path.join(dir_path, "intents.json")

model = pickle.load(open(model_path, "rb"))
lbl_encoder = pickle.load(open(lbl_encoder_path, "rb"))
all_words = pickle.load(open(all_words_path, "rb"))
with open(intents_path, "r", encoding="utf-8") as f:
    intents = json.load(f)

def get_chatbot_response(user_text: str) -> str:
    sent_tokens = nltk.word_tokenize(user_text)
    sent_tokens = [lemmatizer.lemmatize(word.lower()) for word in sent_tokens]

    bag = [0] * len(all_words)
    for s in sent_tokens:
        for i, w in enumerate(all_words):
            if w == s:
                bag[i] = 1
    
    bag = np.array(bag)
    results = model.predict_proba([bag])[0]
    
    CONFIDENCE_THRESHOLD = 0.75
    results_index = np.argmax(results)
    
    if results[results_index] > CONFIDENCE_THRESHOLD:
        tag = lbl_encoder.inverse_transform([results_index])[0]
        for intent in intents['intents']:
            if intent['tag'] == tag:
                response = random.choice(intent['responses'])
                return response
    
    return "I'm sorry, I don't quite understand. Could you rephrase that?"