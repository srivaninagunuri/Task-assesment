import os
import streamlit as st
import chromadb
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer

# ---------------- CONFIG ----------------
st.set_page_config(page_title="PDF RAG Chat", layout="centered")

# ---------------- LOAD ENV ----------------
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------------- EMBEDDING MODEL ----------------
@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

embedding_model = load_embedding_model()

# ---------------- VECTOR STORE ----------------
@st.cache_resource
def load_vectorstore():
    client_db = chromadb.PersistentClient(path="data")
    return client_db.get_collection("pdf_documents")

collection = load_vectorstore()

# ---------------- FUNCTIONS ----------------
def retrieve_chunks(query, top_k=3):
    query_embedding = embedding_model.encode(query)

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k
    )
    return results["documents"][0]

def generate_answer(query):
    chunks = retrieve_chunks(query)

    context = "\n\n".join(chunks)
    context = context[:3000]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "Answer strictly using the provided context."
            },
            {
                "role": "user",
                "content": f"""
Context:
{context}

Question:
{query}
"""
            }
        ],
        temperature=0.3,
        max_tokens=400
    )

    return response.choices[0].message.content

# ---------------- UI ----------------
st.title("📄 PDF Question Answering (RAG)")

st.write("Ask questions based on the uploaded PDFs.")

query = st.text_input("Enter your question:")

if st.button("Ask"):
    if query.strip():
        with st.spinner("Thinking..."):
            answer = generate_answer(query)
        st.success("Answer:")
        st.write(answer)
    else:
        st.warning("Please enter a question.")
