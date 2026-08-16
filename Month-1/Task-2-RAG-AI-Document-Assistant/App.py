import asyncio
import nest_asyncio
import os
import streamlit as st
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA


# ---- Async Fix ----
try:
    asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

nest_asyncio.apply()

# ---- Load API Key ----
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# ---- Page Config ----
st.set_page_config(page_title="AI Document Assistant", page_icon="📚", layout="wide")

st.markdown("""
<h1 style='text-align: center; color: #4CAF50;'>
📚 AI Document Assistant
</h1>
""", unsafe_allow_html=True)


# ---- Sidebar ----
with st.sidebar:
    st.header("📂 Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload files",
        type=["pdf", "txt", "docx"],
        accept_multiple_files=True
    )

    st.markdown("---")
    st.header("⚙️ Settings")
    chunk_size = st.slider("Chunk Size", 500, 2000, 1500)
    chunk_overlap = st.slider("Chunk Overlap", 0, 500, 200)

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []

    st.markdown("---")
    st.info("LangChain + Gemini + HuggingFace + FAISS")


# ---- Load Models ----
@st.cache_resource
def load_models():
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key=api_key
    )

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return llm, embeddings


llm, embeddings = load_models()


# ---- Session ----
if "messages" not in st.session_state:
    st.session_state.messages = []

if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None


VECTOR_PATH = "vectorstore"


# ---- Process Files ----
if uploaded_files:

    all_docs = []

    with st.spinner("Processing documents..."):

        for uploaded_file in uploaded_files:

            file_path = f"temp_{uploaded_file.name}"

            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            if uploaded_file.name.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
            elif uploaded_file.name.endswith(".docx"):
                loader = Docx2txtLoader(file_path)
            else:
                loader = TextLoader(file_path, encoding="utf-8")

            docs = loader.load()
            all_docs.extend(docs)

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        chunks = splitter.split_documents(all_docs)

        # Create FAISS
        vectorstore = FAISS.from_documents(chunks, embeddings)

        # Save locally
        vectorstore.save_local(VECTOR_PATH)

        retriever = vectorstore.as_retriever()

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            return_source_documents=True
        )

        st.session_state.qa_chain = qa_chain

    st.toast("Documents processed & saved! ✅")


# ---- Load Existing VectorStore (if exists) ----
elif os.path.exists(VECTOR_PATH):

    vectorstore = FAISS.load_local(
        VECTOR_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    retriever = vectorstore.as_retriever()

    st.session_state.qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )


# ---- Chat UI ----
if st.session_state.qa_chain:

    user_query = st.chat_input("Ask something about your documents...")

    if user_query:

        st.session_state.messages.append(
            {"role": "user", "content": user_query}
        )

        with st.spinner("Thinking... 🤔"):
            response = st.session_state.qa_chain(user_query)
            answer = response["result"]
            sources = response["source_documents"]

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

        st.session_state.last_sources = sources

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if "last_sources" in st.session_state:
        st.markdown("---")
        st.subheader("📎 Sources")

        for i, doc in enumerate(st.session_state.last_sources, 1):
            with st.expander(f"📄 Source {i}"):
                st.write("Metadata:", doc.metadata)
                st.write(doc.page_content[:500])

else:
    st.info("👈 Upload documents to begin.")