
```markdown
# AI Customer Support Chatbot 🤖

An NLP-based customer support chatbot built using Python and Flask. The chatbot matches user queries with relevant FAQ responses using TF-IDF and Cosine Similarity.

## Features

- FAQ-based question answering
- TF-IDF text vectorization
- Cosine Similarity for query matching
- Flask web interface
- Fallback response for unknown queries
- Simple and lightweight architecture

## Tech Stack

- Python
- Flask
- Pandas
- Scikit-learn
- NLP
- HTML
- CSS
- JavaScript

## How It Works

1. User enters a question.
2. The question is converted into a TF-IDF vector.
3. The chatbot compares it with FAQ questions.
4. Cosine Similarity finds the most relevant match.
5. The corresponding FAQ answer is returned.
6. If no suitable match is found, a fallback response is provided.

## Installation

```bash
pip install -r requirements.txt

Run
python app.py