from flask import Flask, request, jsonify, render_template
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch

app = Flask(__name__)

# -----------------------------
# Load FAQ dataset
# -----------------------------
faq_path = os.path.join(os.getcwd(), "faq.csv")
faq_df = pd.read_csv(faq_path)

# Clean text function
def clean_text(text):
    text = re.sub(r'\r\n', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip().lower()

# Preprocess dataset questions
faq_df['question_clean'] = faq_df['query'].apply(clean_text)

# Vectorizer for similarity matching
# vectorizer = TfidfVectorizer()
vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1,2))
faq_vectors = vectorizer.fit_transform(faq_df['question_clean'])

# -----------------------------
# Optional: Load T5 model (future use)
# -----------------------------
model_path = os.path.join(os.getcwd(), "chatbot_model")
if os.path.exists(model_path):
    model = T5ForConditionalGeneration.from_pretrained(model_path)
    tokenizer = T5Tokenizer.from_pretrained(model_path)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    model.eval()
else:
    model = None

def chatbot(user_input):
    user_input_clean = clean_text(user_input)
    user_vec = vectorizer.transform([user_input_clean])

    similarity = cosine_similarity(user_vec, faq_vectors)

    max_idx = similarity.argmax()
    max_score = similarity[0, max_idx]

    print("User:", user_input)
    print("Best Match:", faq_df.loc[max_idx,'query'])
    print("Score:", max_score)

    if max_score > 0.2:
        return faq_df.loc[max_idx, 'response']
    else:
        return "Sorry, I couldn't understand your question."

# -----------------------------
# Flask Routes
# -----------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "")
    if not user_msg:
        return jsonify({"error": "Message required"}), 400
    response = chatbot(user_msg)
    return jsonify({"response": response})

# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)