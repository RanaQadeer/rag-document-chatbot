# 📄 RAG Document Chatbot

An AI-powered chatbot that lets you upload PDF documents and ask questions about them using Retrieval-Augmented Generation (RAG).

## 🚀 Features
- Upload multiple PDF documents
- Ask questions in natural language
- AI answers based strictly on your documents
- Conversation memory — asks follow-up questions naturally

## 🛠️ Tech Stack
- Python
- Streamlit
- OpenAI / Groq API
- PyPDF2

## ⚙️ How It Works
1. Upload your PDF documents
2. The app extracts and chunks the text
3. Your question is matched to the most relevant chunks
4. An LLM generates an answer based on the context

## 📦 Installation
```bash
git clone https://github.com/RanaQadeer/rag-document-chatbot.git
cd rag-document-chatbot
pip install -r requirements.txt
streamlit run app.py
```

## 🔑 Environment Variables
Create a `.env` file with:
```
OPENAI_API_KEY=your-api-key-here
```
