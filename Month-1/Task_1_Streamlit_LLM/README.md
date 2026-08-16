```markdown
# 💻 Task 1 - Streamlit Local LLM Interface

A fast, lightweight, and completely private local AI Chat Application built using **Streamlit** and **Ollama**. This application allows users to interact with open-source Large Language Models (like Llama 3, Mistral, Phi-3) running directly on their local machine without relying on external cloud APIs.

---

## 📌 Features

- 🔒 **100% Local & Private:** No API keys required. All processing happens on your local hardware.
- ⚡ **Real-time Response Streaming:** Real-time token streaming for a smoother chat interface.
- 🧠 **Context-Aware Memory:** Maintains full chat history using Ollama's `/api/chat` endpoint.
- 🎛️ **Dynamic Model Selection:** Switch between different installed Ollama models directly from the UI sidebar.
- 🎨 **Clean & Custom UI:** Enhanced with custom CSS for improved readability and chat bubbles.
- 🔄 **Conversation Reset:** One-click button to clear chat history and restart.

---

## 🛠️ Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/)
- **Backend / LLM Runner:** [Ollama](https://ollama.com/)
- **Programming Language:** Python 3.9+
- **HTTP Client:** Requests

---

## ⚙️ Prerequisites & Setup

### 1. Install Ollama
Download and install Ollama for your operating system from the official website:
👉 [https://ollama.com](https://ollama.com)

Once installed, pull your desired model using Terminal / Command Prompt:
```bash
ollama pull llama3:latest

```

Ensure the Ollama service is running in the background:

```bash
ollama serve

```

### 2. Clone the Repository

```bash
git clone [https://github.com/SajadaliAI/Generative-AI-Internship-Portfolio.git](https://github.com/SajadaliAI/Generative-AI-Internship-Portfolio.git)
cd Generative-AI-Internship-Portfolio/Month-1/Task_1_Streamlit_LLM

```

### 3. Install Python Dependencies

Install the required packages using `pip`:

```bash
pip install streamlit requests

```

---

## 🚀 How to Run the Application

1. Make sure Ollama is active on your machine (`http://localhost:11434`).
2. Run the Streamlit app:
```bash
streamlit run app.py

```


3. Open your browser and navigate to `http://localhost:8501`.

---

## 📂 Project Structure

```text
Task_1_Streamlit_LLM/
│
├── app.py          # Main Streamlit application logic
└── README.md       # Project documentation

```

---

## 💡 How to Use

1. Enter your installed Ollama model name in the sidebar (Default: `llama3:latest`).
2. Type your message in the chat input at the bottom.
3. The LLM will stream the output back to the screen while remembering the context of your conversation.
4. Click **Reset Conversation** in the sidebar whenever you want to start a fresh chat.
```
