import json
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import pickle
import os

# --- THIS IS THE UPDATED PART ---
# Download necessary NLTK data (only runs if needed)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError: # CORRECTED EXCEPTION
    print("Downloading 'punkt' package...")
    nltk.download('punkt')
try:
    nltk.data.find('corpora/wordnet')
except LookupError: # CORRECTED EXCEPTION
    print("Downloading 'wordnet' package...")
    nltk.download('wordnet')
# --------------------------------

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Get the absolute path to the directory where the script is located
dir_path = os.path.dirname(os.path.realpath(__file__))
intents_path = os.path.join(dir_path, 'intents.json')

# Load intents file using the full path
with open(intents_path, "r", encoding="utf-8") as f:
    intents = json.load(f)

# (The rest of your code is perfect and remains the same)
# ...
all_words = []
tags = []
xy = []
for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']:
        w = nltk.word_tokenize(pattern)
        all_words.extend(w)
        xy.append((w, tag))

ignore_chars = ['?', '!', '.', ',']
all_words = [lemmatizer.lemmatize(w.lower()) for w in all_words if w not in ignore_chars]
all_words = sorted(set(all_words))
tags = sorted(set(tags))

X_train = []
y_train = []
for (pattern_sentence, tag) in xy:
    bag = []
    pattern_words = [lemmatizer.lemmatize(w.lower()) for w in pattern_sentence]
    for w in all_words:
        bag.append(1) if w in pattern_words else bag.append(0)
    X_train.append(bag)
    y_train.append(tag)

X_train = np.array(X_train)
lbl_encoder = LabelEncoder()
y_train = lbl_encoder.fit_transform(y_train)

model = SVC(kernel='linear', probability=True)
model.fit(X_train, y_train)

# Replace the old, incomplete lines with these:
pickle.dump(model, open(os.path.join(dir_path, "chatbot_model.pkl"), "wb"))
pickle.dump(lbl_encoder, open(os.path.join(dir_path, "label_encoder.pkl"), "wb"))
pickle.dump(all_words, open(os.path.join(dir_path, "all_words.pkl"), "wb"))