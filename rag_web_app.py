import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from PIL import Image
import tempfile

# ---- Configuration ----
st.set_page_config(page_title="Gemini PDF Chat", layout="wide", page_icon="📄")

# ---- Sidebar (Logo + Chat History) ----
with st.sidebar:
    try:
        logo = Image.open("logo.png")
        st.image(logo, width=150)
    except:
        st.markdown("🧠 **Gemini PDF Chat**")
    st.markdown("---")
    st.markdown("### 📚 Previous Questions")
    if "chat_history" in st.session_state:
        for idx, (q, _) in enumerate(st.session_state.chat_history):
            st.markdown(f"**{idx+1}.** {q[:50]}...")

# ---- Gemini API Key ----
api_key = "AIzaSyAKZViSxSXD9Zc3c-m_CpcsBQZAGPlP0-o"

# ---- Session State Init ----
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None

# ---- Title & Upload ----
st.title("RAGified Reader")
uploaded_file = st.file_uploader("📤 Upload a PDF file", type="pdf")

# ---- PDF Processing ----
if uploaded_file and st.session_state.qa_chain is None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    st.info("🔍 Extracting content and indexing...")
    loader = PyPDFLoader(tmp_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
    vectordb = Chroma.from_documents(chunks, embedding=embeddings)
    retriever = vectordb.as_retriever(search_kwargs={"k": 10})

    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=api_key)
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=model,
        retriever=retriever,
        return_source_documents=False
    )
    st.session_state.qa_chain = qa_chain
    st.success("✅ PDF indexed! Start chatting below.")

# ---- Chat Interface ----
if st.session_state.qa_chain:
    user_input = st.chat_input("💬 Ask your question here...")
    if user_input:
        with st.spinner("🤖 Generating response..."):
            result = st.session_state.qa_chain({
                "question": user_input,
                "chat_history": st.session_state.chat_history
            })
            st.session_state.chat_history.append((user_input, result["answer"]))

    # Display Chat History (ChatGPT Style)
    for q, a in st.session_state.chat_history:
        with st.chat_message("user", avatar="👤"):
            st.markdown(q)
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(a)
