# predict.py
import json
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
import pickle
from gtts import gTTS
import os
import playsound  # To play audio

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Load data and trained model
intents = json.load(open("intents.json", encoding="utf-8"))
model = pickle.load(open("chatbot_model.pkl", "rb"))
lbl_encoder = pickle.load(open("label_encoder.pkl", "rb"))
all_words = pickle.load(open("all_words.pkl", "rb"))

# ------------------------
# Helper functions
# ------------------------

def tokenize(sentence):
    return nltk.word_tokenize(sentence)

def lemmatize_words(words):
    return [lemmatizer.lemmatize(w.lower()) for w in words]

def bag_of_words(sentence, all_words):
    sentence_words = lemmatize_words(tokenize(sentence))
    bag = np.zeros(len(all_words), dtype=int)
    for idx, w in enumerate(all_words):
        if w in sentence_words:
            bag[idx] = 1
    return bag

def speak(text, lang='mr'):
    tts = gTTS(text=text, lang=lang)
    filename = "temp.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

# ------------------------
# Main prediction loop
# ------------------------

print("कृपया बोलून किंवा टाइप करून प्रश्न विचारा (type 'exit' to quit):")

while True:
    # Get input from user
    sentence = input("आपण: ")
    if sentence.lower() == "exit":
        print("चॅटबॉट बंद केला.")
        break

    # Prepare input for model
    bow = bag_of_words(sentence, all_words)
    bow = bow.reshape(1, -1)

    # Predict intent
    result = model.predict(bow)
    tag = lbl_encoder.inverse_transform(result)[0]

    # Choose random response from intents
    for intent in intents["intents"]:
        if intent["tag"] == tag:
            response = np.random.choice(intent["responses"])
            break

    print("चॅटबॉट:", response)
    speak(response)  # Speak response in Marathi
