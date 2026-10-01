
import streamlit as st
from google import genai
from dotenv import load_dotenv
from pypdf import PdfReader
import chromadb
import os
import uuid

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Gemini RAG | AI PDF Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# PROFESSIONAL CSS
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --primary: #7454e8;
    --primary-dark: #5b3bc5;
    --background: #f5f6fc;
    --card: #ffffff;
    --text: #20243a;
    --muted: #747b91;
    --border: #e8e9f2;
}

.stApp {
    background: var(--background);
    font-family: 'Inter', sans-serif;
    color: var(--text);
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1200px;
    padding: 2rem 2rem 4rem 2rem;
}

/* Hide default Streamlit decorations */
#MainMenu, footer {
    visibility: hidden;
}

/* Hero section */
.hero {
    background: linear-gradient(120deg, #211c4d 0%, #49339c 55%, #7959e8 100%);
    padding: 42px 44px;
    border-radius: 24px;
    color: white;
    margin-bottom: 30px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 15px 40px rgba(75, 53, 155, 0.16);
}

.hero::after {
    content: "";
    position: absolute;
    width: 240px;
    height: 240px;
    border-radius: 50%;
    background: rgba(255,255,255,0.06);
    right: -60px;
    top: -100px;
}

.hero-tag {
    display: inline-block;
    padding: 7px 13px;
    border: 1px solid rgba(255,255,255,0.23);
    background: rgba(255,255,255,0.10);
    border-radius: 50px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.5px;
    margin-bottom: 17px;
}

.hero h1 {
    font-size: 36px;
    font-weight: 800;
    color: white;
    margin: 0 0 12px 0;
    letter-spacing: -1.1px;
}

.hero p {
    color: #e5dfff;
    font-size: 15px;
    line-height: 1.7;
    max-width: 650px;
    margin-bottom: 0;
}

/* Section titles */
.section-heading {
    font-size: 20px;
    font-weight: 750;
    color: var(--text);
    margin: 12px 0 5px 0;
}

.section-subtitle {
    color: var(--muted);
    font-size: 13px;
    margin-bottom: 18px;
}

/* Cards */
.panel {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 24px;
    box-shadow: 0 5px 20px rgba(30, 36, 70, 0.035);
    margin-bottom: 18px;
}

.metric-card {
    background: white;
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px;
    min-height: 112px;
    box-shadow: 0 5px 18px rgba(30, 36, 70, 0.035);
}

.metric-label {
    color: var(--muted);
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 10px;
}

.metric-value {
    font-size: 25px;
    font-weight: 800;
    color: var(--text);
}

.metric-icon {
    font-size: 20px;
    margin-bottom: 7px;
}

/* Upload area */

/* PDF Upload Area */
[data-testid="stFileUploader"] {
    background: #faf9ff !important;
    border: 1.5px dashed #b9a9f3 !important;
    border-radius: 16px !important;
    padding: 16px !important;
}

/* Upload dropzone */
[data-testid="stFileUploaderDropzone"] {
    background: #f8f7ff !important;
    border: none !important;
    border-radius: 12px !important;
}

/* Upload button */
[data-testid="stFileUploaderDropzone"] button {
    background: #7454e8 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 9px !important;
    padding: 10px 20px !important;
    font-weight: 600 !important;
}

/* Force visible button text and icon */
[data-testid="stFileUploaderDropzone"] button,
[data-testid="stFileUploaderDropzone"] button * {
    color: #ffffff !important;
    fill: #ffffff !important;
    opacity: 1 !important;
}

/* Hover effect */
[data-testid="stFileUploaderDropzone"] button:hover {
    background: #5b3bc5 !important;
}

/* Upload instructions */
[data-testid="stFileUploaderDropzone"] span,
[data-testid="stFileUploaderDropzone"] small,
[data-testid="stFileUploaderDropzone"] p {
    color: #555b75 !important;
}

/* Uploaded file name */
[data-testid="stFileUploaderFileName"] {
    color: #292442 !important;
    font-weight: 600 !important;
}

[data-testid="stFileUploader"] section {
    border: none;
}

/* Input fields */
.stTextInput input {
    border-radius: 12px;
    border: 1px solid #dedfec;
    background: #ffffff;
    padding: 13px 15px;
    color: var(--text);
    min-height: 48px;
}

.stTextInput input:focus {
    border-color: var(--primary);
    box-shadow: 0 0 0 2px rgba(116,84,232,0.12);
}

/* Buttons */
.stButton > button {
    background: linear-gradient(120deg, #7657e8, #5d40c7);
    color: white;
    border: none;
    border-radius: 11px;
    padding: 11px 22px;
    min-height: 45px;
    font-size: 14px;
    font-weight: 650;
    transition: all 0.2s ease;
    box-shadow: 0 5px 14px rgba(104, 74, 211, 0.17);
}

.stButton > button:hover {
    background: linear-gradient(120deg, #6242d1, #4930aa);
    color: white;
    transform: translateY(-1px);
    box-shadow: 0 8px 18px rgba(104, 74, 211, 0.25);
}

.stButton > button:focus {
    color: white;
    border: 1px solid #8d75ed;
}

/* Answer card */
.answer-card {
    background: #ffffff;
    border: 1px solid #e5defb;
    border-left: 4px solid #7657e8;
    border-radius: 15px;
    padding: 24px;
    line-height: 1.8;
    color: #34344e;
    font-size: 15px;
    box-shadow: 0 6px 20px rgba(30, 36, 70, 0.04);
    margin-top: 10px;
    white-space: pre-wrap;
}

/* Status pill */
.status-pill {
    display: inline-block;
    padding: 7px 12px;
    background: #eaf8ef;
    color: #248348;
    border-radius: 50px;
    font-size: 12px;
    font-weight: 650;
}

/* Expander */
[data-testid="stExpander"] {
    background: white;
    border: 1px solid var(--border);
    border-radius: 13px;
    overflow: hidden;
}

/* Divider */
hr {
    border-color: var(--border);
    margin: 28px 0;
}

/* Footer */
.footer {
    text-align: center;
    padding: 25px 10px 5px;
    color: #858ba0;
    font-size: 12px;
}

/* Responsive */
@media (max-width: 768px) {
    .block-container {
        padding: 1rem 1rem 3rem 1rem;
    }

    .hero {
        padding: 28px 22px;
    }

    .hero h1 {
        font-size: 27px;
    }

    .panel {
        padding: 17px;
    }
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# ENVIRONMENT AND CLIENT
# =========================================================

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("GEMINI_API_KEY is missing. Please check your .env file.")
    st.stop()

client = genai.Client(api_key=API_KEY)

# =========================================================
# CHROMADB
# =========================================================

if "chroma_client" not in st.session_state:
    st.session_state.chroma_client = chromadb.Client()

chroma_client = st.session_state.chroma_client

if "collection" not in st.session_state:
    st.session_state.collection = chroma_client.get_or_create_collection(
        name="gemini_rag_collection"
    )

collection = st.session_state.collection

# =========================================================
# SESSION STATE
# =========================================================

if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False

if "document_name" not in st.session_state:
    st.session_state.document_name = ""

if "chunk_count" not in st.session_state:
    st.session_state.chunk_count = 0

if "page_count" not in st.session_state:
    st.session_state.page_count = 0

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# =========================================================
# HERO HEADER
# =========================================================

st.markdown("""
<div class="hero">
    <div class="hero-tag">✦ POWERED BY GOOGLE GEMINI AI</div>
    <h1>📚 Gemini PDF Assistant</h1>
    <p>
        Upload your PDF, explore its content, and get accurate,
        context-aware answers with Retrieval-Augmented Generation.
        Your documents, your questions, intelligent answers.
    </p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# PDF EXTRACTION
# =========================================================

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text, len(reader.pages)

# =========================================================
# CHUNKING
# =========================================================

def create_chunks(text, chunk_size=1000):
    chunks = []

    for start in range(0, len(text), chunk_size):
        chunk = text[start:start + chunk_size]

        if chunk.strip():
            chunks.append(chunk)

    return chunks

# =========================================================
# EMBEDDINGS
# =========================================================

def create_embedding(text):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

    return response.embeddings[0].values

# =========================================================
# STORE CHUNKS
# =========================================================

def store_chunks(chunks):
    global collection

    try:
        chroma_client.delete_collection("gemini_rag_collection")
    except Exception:
        pass

    collection = chroma_client.get_or_create_collection(
        name="gemini_rag_collection"
    )

    embeddings = []

    progress = st.progress(0, text="Generating embeddings...")

    for i, chunk in enumerate(chunks):
        embedding = create_embedding(chunk)
        embeddings.append(embedding)

        progress.progress(
            (i + 1) / len(chunks),
            text=f"Embedding chunk {i + 1} of {len(chunks)}"
        )

    ids = [f"chunk_{uuid.uuid4().hex}" for _ in chunks]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings
    )

    progress.empty()
    st.session_state.collection = collection

    return len(chunks)

# =========================================================
# GENERATE ANSWER
# =========================================================

def generate_answer(question, context):
    prompt = f"""
You are a helpful AI document assistant.

Answer the user's question using ONLY the information
provided in the context below.

If the answer is not available in the context,
say exactly:
"I could not find the answer in the uploaded document."

Do not invent facts or use outside information.
Provide a clear, well-structured answer.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text or "No answer was generated."

# =========================================================
# DOCUMENT UPLOAD SECTION
# =========================================================

st.markdown('<div class="section-heading">📄 Upload your document</div>',
            unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Upload a PDF to begin your AI-powered document conversation.</div>',
    unsafe_allow_html=True
)

with st.container(border=True):
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        help="Select a text-based PDF document."
    )

    if uploaded_file is not None:
        st.markdown(
            f'<div class="status-pill">✓ Selected: {uploaded_file.name}</div>',
            unsafe_allow_html=True
        )

        if st.button("⚡ Process PDF", use_container_width=True):
            try:
                with st.spinner("Extracting document text..."):
                    text, page_count = extract_text_from_pdf(uploaded_file)

                if not text.strip():
                    st.error(
                        "No readable text found. This PDF may contain scanned pages."
                    )
                else:
                    chunks = create_chunks(text)

                    with st.spinner("Creating embeddings and indexing document..."):
                        number_of_chunks = store_chunks(chunks)

                    st.session_state.pdf_processed = True
                    st.session_state.document_name = uploaded_file.name
                    st.session_state.chunk_count = number_of_chunks
                    st.session_state.page_count = page_count
                    st.session_state.chat_history = []

                    st.success("Your document is ready! You can now ask questions.")

            except Exception as e:
                st.error(f"Processing failed: {e}")

# =========================================================
# DOCUMENT DASHBOARD
# =========================================================

if st.session_state.pdf_processed:
    st.divider()

    st.markdown(
        '<div class="section-heading">📊 Document overview</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">📄</div>
            <div class="metric-label">DOCUMENT</div>
            <div style="font-size:14px;font-weight:700;word-break:break-word;">
                {st.session_state.document_name}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">📑</div>
            <div class="metric-label">TOTAL PAGES</div>
            <div class="metric-value">{st.session_state.page_count}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">🧩</div>
            <div class="metric-label">TEXT CHUNKS</div>
            <div class="metric-value">{st.session_state.chunk_count}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        '<div class="status-pill">● Document indexed and ready</div>',
        unsafe_allow_html=True
    )

# =========================================================
# CHAT SECTION
# =========================================================

if st.session_state.pdf_processed:
    st.divider()

    st.markdown(
        '<div class="section-heading">💬 Ask your document</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="section-subtitle">Ask questions and get answers based on your uploaded PDF.</div>',
        unsafe_allow_html=True
    )

    with st.container(border=True):
        question = st.text_input(
            "Your question",
            placeholder="e.g. What are the key points discussed in this document?",
            key="question_input"
        )

        if st.button("🔍 Generate Answer", use_container_width=True):
            if not question.strip():
                st.warning("Please enter a question.")
            else:
                try:
                    with st.spinner("Searching relevant document content..."):
                        question_embedding = create_embedding(question)

                        results = collection.query(
                            query_embeddings=[question_embedding],
                            n_results=min(3, collection.count())
                        )

                    documents = results["documents"][0]
                    context = "\n\n".join(documents)

                    with st.spinner("Gemini is generating your answer..."):
                        answer = generate_answer(question, context)

                    st.session_state.chat_history.insert(0, {
                        "question": question,
                        "answer": answer,
                        "context": documents
                    })

                except Exception as e:
                    st.error(f"Could not generate answer: {e}")

    # =====================================================
    # DISPLAY CHAT HISTORY
    # =====================================================

    for i, chat in enumerate(st.session_state.chat_history):
        st.markdown("### 🤖 AI Response")

        st.markdown(
            f'<div class="answer-card">{chat["answer"]}</div>',
            unsafe_allow_html=True
        )

        st.markdown(f"**You asked:** {chat['question']}")

        with st.expander("📖 View retrieved context"):
            for j, doc in enumerate(chat["context"]):
                st.markdown(f"**Retrieved passage {j + 1}**")
                st.write(doc)
                if j < len(chat["context"]) - 1:
                    st.divider()

        st.markdown("")

    if st.session_state.chat_history:
        if st.button("🗑️ Clear conversation"):
            st.session_state.chat_history = []
            st.rerun()

# =========================================================
# EMPTY STATE
# =========================================================

else:
    st.markdown("""
    <div class="panel" style="text-align:center;padding:35px 20px;">
        <div style="font-size:42px;margin-bottom:12px;">✨</div>
        <div style="font-size:19px;font-weight:750;color:#27263e;">
            Your AI workspace is ready
        </div>
        <p style="font-size:13px;color:#777e93;margin-top:9px;">
            Upload and process a PDF to unlock intelligent document search
            and AI-powered question answering.
        </p>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">
    ✦ Gemini PDF Assistant &nbsp; | &nbsp; Built with Streamlit,
    Google Gemini AI and ChromaDB
    <br><br>
    Intelligent document understanding, simplified.
</div>
""", unsafe_allow_html=True)