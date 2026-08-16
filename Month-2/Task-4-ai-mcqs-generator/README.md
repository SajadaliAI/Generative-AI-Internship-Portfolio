
---

# 5. AI MCQs Generator README

Tumhara current README **already strong hai**. Bas `.env` aur generated PDF ko GitHub par mat push karna.

README mein ye rakho:

```markdown
# 🧠 AI MCQs Generator

An AI-powered web application that generates Multiple Choice Questions (MCQs) from a topic or uploaded PDF using LangChain and Groq LLM.

## Features

- Generate MCQs from a topic
- Generate MCQs from uploaded PDF
- Select difficulty level
- Generate answer keys
- Generate question papers as PDF
- Structured JSON output
- Streamlit web interface

## Tech Stack

- Python
- LangChain
- Groq
- Llama 3.1
- Streamlit
- PyPDF
- ReportLab

## How It Works

1. User enters a topic or uploads a PDF.
2. PDF text is extracted when a document is uploaded.
3. A prompt is created using LangChain.
4. Groq LLM generates the MCQs.
5. The response is parsed and formatted.
6. The generated question paper can be downloaded as a PDF.

## Installation

```bash
pip install -r requirements.txt

Run
streamlit run UI.py