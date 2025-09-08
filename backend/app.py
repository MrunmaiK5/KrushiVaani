from fastapi import FastAPI

# Routers
from backend.routes.fertilizer_routes import fertilizer_router
from backend.routes.crop_routes import router as crop_router

from pydantic import BaseModel
import json
import numpy as np
import pickle
import nltk
from nltk.stem import WordNetLemmatizer

# ------------------------
# Initialize FastAPI
# ------------------------
app = FastAPI(title="Krushivaani Backend")

app.include_router(fertilizer_router, prefix="/fertilizer", tags=["Fertilizer"])
app.include_router(crop_router, prefix="/crop", tags=["Crop"])

# ------------------------
# Load Chatbot Model
# ------------------------
model = pickle.load(open("ml_models/chatbot/chatbot_model.pkl", "rb"))
lbl_encoder = pickle.load(open("ml_models/chatbot/label_encoder.pkl", "rb"))
all_words = pickle.load(open("ml_models/chatbot/all_words.pkl", "rb"))
intents = json.load(open("ml_models/chatbot/intents.json", encoding="utf-8"))
lemmatizer = WordNetLemmatizer()

# ------------------------
# Helper Functions
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

# ------------------------
# Chatbot Request Model
# ------------------------
class ChatRequest(BaseModel):
    message: str

# ------------------------
# Chatbot Route
# ------------------------
@app.post("/chatbot", tags=["Chatbot"])
async def chatbot_response(request: ChatRequest):
    sentence = request.message
    bow = bag_of_words(sentence, all_words).reshape(1, -1)
    result = model.predict(bow)
    tag = lbl_encoder.inverse_transform(result)[0]

    # Select response
    response = ""
    for intent in intents["intents"]:
        if intent["tag"] == tag:
            response = np.random.choice(intent["responses"])
            break

    return {"response": response}

# ------------------------
# Home Route
# ------------------------
@app.get("/")
def home():
    return {"message": "Welcome to Krushivaani Backend"}
