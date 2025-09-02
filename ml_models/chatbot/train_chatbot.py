import json
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import pickle

nltk.download('punkt')
nltk.download('wordnet')

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Load intents file
with open("intents.json", "r", encoding="utf-8") as f:
    intents = json.load(f)

# Prepare data
all_words = []
tags = []
xy = []

for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']:
        # Tokenize
        w = nltk.word_tokenize(pattern)
        all_words.extend(w)
        xy.append((w, tag))

# Lemmatize and lower-case all words
ignore_chars = ['?', '!', '.', ',']
all_words = [lemmatizer.lemmatize(w.lower()) for w in all_words if w not in ignore_chars]
all_words = sorted(set(all_words))
tags = sorted(set(tags))

# Prepare training data
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

# Encode output labels
lbl_encoder = LabelEncoder()
y_train = lbl_encoder.fit_transform(y_train)

# Train model
model = SVC(kernel='linear', probability=True)
model.fit(X_train, y_train)

# Save model and encoder
pickle.dump(model, open("chatbot_model.pkl", "wb"))
pickle.dump(lbl_encoder, open("label_encoder.pkl", "wb"))
pickle.dump(all_words, open("all_words.pkl", "wb"))

print("Training complete. Model saved as chatbot_model.pkl")
