import streamlit as st
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        reader = PdfReader(pdf)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted
    return text

def split_text(text, chunk_size=2000, overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

def find_relevant_chunks(query, chunks, top_k=3):
    query_words = set(query.lower().split())
    scored = []
    for chunk in chunks:
        chunk_words = set(chunk.lower().split())
        score = len(query_words & chunk_words)
        scored.append((score, chunk))
    scored.sort(reverse=True)
    return [chunk for _, chunk in scored[:top_k]]

def get_answer(question, chunks, chat_history):
    relevant = find_relevant_chunks(question, chunks)
    context = "\n\n".join(relevant)

    messages = [
        {
            "role": "system",
            "content": f"""You are a helpful assistant that answers questions based on the provided document context.
            
Context from documents:
{context}

Answer based on the context above. If the answer isn't in the context, say so."""
        }
    ]

    for msg in chat_history:
        messages.append(msg)

    messages.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content

def main():
    st.set_page_config(page_title="Chat with PDFs", page_icon="📄")
    st.title("📄 RAG Document Chatbot")
    st.write("Upload your PDFs and ask anything about them!")

    if "chunks" not in st.session_state:
        st.session_state.chunks = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    with st.sidebar:
        st.subheader("📂 Upload Documents")
        pdf_docs = st.file_uploader(
            "Upload PDFs",
            accept_multiple_files=True,
            type="pdf"
        )
        if st.button("Process PDFs"):
            if not pdf_docs:
                st.warning("Please upload at least one PDF.")
            else:
                with st.spinner("Processing..."):
                    raw_text = get_pdf_text(pdf_docs)
                    st.session_state.chunks = split_text(raw_text)
                    st.session_state.chat_history = []
                    st.success(f"Done! {len(st.session_state.chunks)} chunks created. Ask away!")

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    question = st.chat_input("Ask a question about your documents...")
    if question:
        if st.session_state.chunks is None:
            st.warning("Please upload and process a PDF first.")
        else:
            with st.chat_message("user"):
                st.write(question)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    answer = get_answer(
                        question,
                        st.session_state.chunks,
                        st.session_state.chat_history
                    )
                    st.write(answer)

            st.session_state.chat_history.append({"role": "user", "content": question})
            st.session_state.chat_history.append({"role": "assistant", "content": answer})

if __name__ == "__main__":
    main()
