from flask import Flask, request, jsonify, render_template
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

app = Flask(__name__)

# -----------------------------
# Load FAQ dataset
# -----------------------------
faq_path = os.path.join(os.getcwd(), "faq.csv")
faq_df = pd.read_csv(faq_path)


# -----------------------------
# Clean text function
# -----------------------------
def clean_text(text):
    text = re.sub(r'\r\n', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip().lower()


# -----------------------------
# Preprocess FAQ questions
# -----------------------------
faq_df['question_clean'] = faq_df['query'].apply(clean_text)


# -----------------------------
# TF-IDF Vectorizer
# -----------------------------
vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2)
)

faq_vectors = vectorizer.fit_transform(
    faq_df['question_clean']
)


# -----------------------------
# Chatbot Logic
# -----------------------------
def chatbot(user_input):
    user_input_clean = clean_text(user_input)

    # Convert user query into TF-IDF vector
    user_vec = vectorizer.transform([user_input_clean])

    # Calculate similarity with FAQ questions
    similarity = cosine_similarity(user_vec, faq_vectors)

    # Find best matching question
    max_idx = similarity.argmax()
    max_score = similarity[0, max_idx]

    print("User:", user_input)
    print("Best Match:", faq_df.loc[max_idx, 'query'])
    print("Score:", max_score)

    # Return answer if similarity is high enough
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