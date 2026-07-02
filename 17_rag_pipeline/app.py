import streamlit as st
import tempfile
import os
from dotenv import load_dotenv

load_dotenv()

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DocMind · RAG Assistant",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@600;700&display=swap');

/* ═══════════════════════════════════════
   GLOBAL RESET & BASE
═══════════════════════════════════════ */
*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    background-color: #080B12 !important;
    color: #C9D1E0 !important;
}

/* hide streamlit default chrome */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ═══════════════════════════════════════
   SIDEBAR
═══════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: #0C0F1A !important;
    border-right: 1px solid #161C2D !important;
    padding-top: 0 !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding: 0 !important;
}
[data-testid="stSidebar"] .block-container {
    padding: 1.5rem 1.25rem 2rem !important;
}

/* sidebar brand strip */
.sb-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 1.25rem 1.25rem 1rem;
    border-bottom: 1px solid #161C2D;
    margin-bottom: 1.25rem;
}
.sb-brand-icon {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, #5B6CFF, #A855F7);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
}
.sb-brand-text { font-family: 'Space Grotesk', sans-serif; font-size: 1.1rem;
                  font-weight: 700; color: #E8EAFF; letter-spacing: -0.02em; }
.sb-brand-sub  { font-size: 0.68rem; color: #4A5270; margin-top: 1px; }

/* sidebar section labels */
.sb-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #3D4560;
    margin: 1.25rem 0 0.5rem;
}

/* role cards */
.role-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px;
    margin-bottom: 0.5rem;
}
.role-card {
    background: #10141F;
    border: 1px solid #1A2035;
    border-radius: 8px;
    padding: 0.5rem 0.6rem;
    cursor: pointer;
    transition: all 0.15s;
    text-align: center;
}
.role-card:hover  { border-color: #5B6CFF; background: #13182A; }
.role-card.active { border-color: #5B6CFF; background: #13182A;
                    box-shadow: 0 0 0 1px #5B6CFF; }
.role-icon { font-size: 1.1rem; margin-bottom: 2px; }
.role-name { font-size: 0.68rem; font-weight: 600; color: #8891B4; }

/* doc card */
.doc-card {
    background: #10141F;
    border: 1px solid #1A2035;
    border-radius: 10px;
    padding: 0.75rem 0.9rem;
    margin-top: 0.4rem;
}
.doc-card-name { font-size: 0.82rem; font-weight: 600; color: #C9D1E0;
                  white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.doc-card-meta { font-size: 0.7rem; color: #4A5270; margin-top: 2px; }
.doc-ready-dot { display: inline-block; width: 7px; height: 7px;
                  background: #22C55E; border-radius: 50%; margin-right: 5px;
                  animation: pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }

/* sidebar footer */
.sb-footer {
    position: absolute; bottom: 1rem; left: 1.25rem; right: 1.25rem;
    font-size: 0.68rem; color: #272E45; text-align: center;
    border-top: 1px solid #111726; padding-top: 0.75rem;
}

/* ═══════════════════════════════════════
   MAIN LAYOUT
═══════════════════════════════════════ */
.main .block-container {
    max-width: 820px !important;
    padding: 2rem 1.5rem 6rem !important;
    margin: 0 auto;
}

/* ── Page header ── */
.page-header {
    display: flex;
    align-items: center;
    gap: 14px;
    padding-bottom: 1.25rem;
    border-bottom: 1px solid #161C2D;
    margin-bottom: 1.5rem;
}
.page-header-icon {
    width: 46px; height: 46px;
    background: linear-gradient(135deg, #5B6CFF 0%, #A855F7 100%);
    border-radius: 13px;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px; flex-shrink: 0;
    box-shadow: 0 0 20px rgba(91,108,255,0.35);
}
.page-header h1 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    color: #E8EAFF !important;
    letter-spacing: -0.03em !important;
    margin: 0 !important; padding: 0 !important;
    background: none !important;
    -webkit-background-clip: unset !important;
    -webkit-text-fill-color: unset !important;
}
.page-header-sub { font-size: 0.8rem; color: #4A5270; margin-top: 1px; }

/* ── Empty state ── */
.empty-state {
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    padding: 4rem 2rem;
    text-align: center;
    gap: 1rem;
}
.empty-icon {
    width: 72px; height: 72px;
    background: #0C0F1A;
    border: 1px solid #1A2035;
    border-radius: 20px;
    display: flex; align-items: center; justify-content: center;
    font-size: 32px;
    margin-bottom: 0.5rem;
}
.empty-title { font-family:'Space Grotesk',sans-serif; font-size:1.15rem;
                font-weight:700; color:#4A5270; }
.empty-sub   { font-size:0.83rem; color:#2D3450; max-width:320px; line-height:1.6; }

/* ── Chat messages ── */
.chat-wrap { display: flex; flex-direction: column; gap: 1rem; margin-bottom: 1rem; }

.msg-row { display: flex; gap: 10px; align-items: flex-start; }
.msg-row.user { flex-direction: row-reverse; }

.avatar {
    width: 34px; height: 34px; border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 15px; flex-shrink: 0; margin-top: 2px;
}
.avatar-user { background: linear-gradient(135deg,#A855F7,#6366F1); }
.avatar-ai   { background: linear-gradient(135deg,#5B6CFF,#06B6D4);
                box-shadow: 0 0 12px rgba(91,108,255,0.3); }

.bubble {
    max-width: 78%;
    padding: 0.85rem 1.1rem;
    border-radius: 4px 14px 14px 14px;
    font-size: 0.9rem;
    line-height: 1.7;
    position: relative;
}
.bubble-user {
    background: #151B2E;
    border: 1px solid #1E2840;
    border-radius: 14px 4px 14px 14px;
    color: #D4D9EF;
}
.bubble-ai {
    background: #0D1120;
    border: 1px solid #192038;
    border-left: 2px solid #5B6CFF;
    color: #C9D1E0;
}
.bubble-meta {
    font-size: 0.67rem;
    font-weight: 600;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    margin-bottom: 0.45rem;
}
.meta-user { color: #7C5AC7; }
.meta-ai   { color: #4B5CC4; }

.source-row { display: flex; flex-wrap: wrap; gap: 4px; margin-top: 0.6rem; }
.src-chip {
    background: #111827;
    border: 1px solid #1E2840;
    border-radius: 5px;
    padding: 0.15rem 0.5rem;
    font-size: 0.67rem;
    color: #3D4D6E;
    font-weight: 500;
}

/* ── Input bar ── */
.input-bar {
    position: fixed;
    bottom: 0; left: 0; right: 0;
    background: linear-gradient(to top, #080B12 70%, transparent);
    padding: 1.25rem 0 1.5rem;
    z-index: 100;
}
.input-inner {
    max-width: 820px;
    margin: 0 auto;
    padding: 0 1.5rem;
    display: flex;
    gap: 10px;
    align-items: center;
}

/* override streamlit input */
[data-testid="stTextInput"] {
    flex: 1;
}
[data-testid="stTextInput"] > div { border: none !important; }
[data-testid="stTextInput"] input {
    background: #0D1120 !important;
    border: 1px solid #1A2240 !important;
    border-radius: 12px !important;
    color: #C9D1E0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    padding: 0.75rem 1rem !important;
    height: 48px !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #5B6CFF !important;
    box-shadow: 0 0 0 3px rgba(91,108,255,0.12) !important;
    outline: none !important;
}
[data-testid="stTextInput"] input::placeholder { color: #2D3655 !important; }

/* buttons */
.stButton > button {
    background: linear-gradient(135deg, #5B6CFF, #A855F7) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 0 1.4rem !important;
    height: 48px !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: 0.01em !important;
    transition: opacity 0.15s, transform 0.1s !important;
    white-space: nowrap !important;
}
.stButton > button:hover  { opacity: 0.88 !important; transform: translateY(-1px) !important; }
.stButton > button:active { transform: translateY(0) !important; }

/* secondary button (clear) */
.stButton.secondary > button {
    background: #10141F !important;
    border: 1px solid #1A2035 !important;
    color: #5A6480 !important;
    font-size: 0.78rem !important;
    padding: 0 0.9rem !important;
    height: 34px !important;
}

/* selectbox */
[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background: #0D1120 !important;
    border: 1px solid #1A2240 !important;
    border-radius: 10px !important;
    color: #C9D1E0 !important;
}
[data-testid="stSelectbox"] [data-baseweb="select"] svg { color: #4A5270 !important; }

/* file uploader */
[data-testid="stFileUploader"] section {
    background: #0D1120 !important;
    border: 1.5px dashed #1A2240 !important;
    border-radius: 12px !important;
    transition: border-color 0.2s !important;
}
[data-testid="stFileUploader"] section:hover {
    border-color: #5B6CFF !important;
}
[data-testid="stFileUploader"] label { color: #4A5270 !important; }

/* spinner */
.stSpinner > div { border-top-color: #5B6CFF !important; }

/* info / warning */
.stAlert { background: #0D1120 !important; border-radius: 10px !important;
            border-color: #1A2240 !important; color: #C9D1E0 !important; }

/* scrollbar */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #1A2035; border-radius: 99px; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def build_vectorstore(file_bytes: bytes, filename: str):
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_mistralai import MistralAIEmbeddings
    from langchain_community.vectorstores import Chroma

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    loader = PyPDFLoader(tmp_path)
    docs   = loader.load()
    os.unlink(tmp_path)

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks   = splitter.split_documents(docs)

    embedding_model = MistralAIEmbeddings(model="mistral-embed")
    vectorstore = Chroma.from_documents(documents=chunks, embedding=embedding_model)
    return vectorstore, len(chunks), len(docs)


def get_answer(query: str, vectorstore, role: str):
    from langchain_mistralai import ChatMistralAI
    from langchain_core.prompts import ChatPromptTemplate

    styles = {
        "🎓 Student":          "Explain clearly and simply, as if teaching a beginner. Use analogies and examples.",
        "🔬 Researcher":       "Give precise, detailed answers. Cite specific sections when possible.",
        "💼 Professional":     "Focus on practical takeaways and actionable insights.",
        "🙂 General User":     "Give a balanced, easy-to-read answer.",
    }
    style = styles.get(role, styles["🙂 General User"])

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 4, "fetch_k": 10, "lambda_mult": 0.5},
    )
    docs    = retriever.invoke(query)
    context = "\n\n".join(d.page_content for d in docs)

    prompt = ChatPromptTemplate.from_messages([
        ("system", f"""You are a helpful AI assistant. {style}
Use ONLY the provided context to answer the question.
If the answer is not present in the context, say: "I could not find the answer in the document." """),
        ("human", "Context:\n{context}\n\nQuestion:\n{question}"),
    ])

    llm      = ChatMistralAI(model="mistral-small-latest")
    response = llm.invoke(prompt.invoke({"context": context, "question": query}))

    sources = []
    for d in docs:
        page = d.metadata.get("page", "?")
        sources.append(f"p.{page+1}" if isinstance(page, int) else str(page))
    return response.content, list(dict.fromkeys(sources))


# ── Session state ─────────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "role" not in st.session_state:
    st.session_state.role = "🙂 General User"


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    # Brand
    st.markdown("""
    <div class="sb-brand">
        <div class="sb-brand-icon">📖</div>
        <div>
            <div class="sb-brand-text">DocMind</div>
            <div class="sb-brand-sub">RAG · PDF Assistant</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Role
    st.markdown('<div class="sb-label">Your Role</div>', unsafe_allow_html=True)
    role = st.selectbox(
        "role",
        ["🙂 General User", "🎓 Student", "🔬 Researcher", "💼 Professional"],
        index=["🙂 General User","🎓 Student","🔬 Researcher","💼 Professional"].index(st.session_state.role),
        label_visibility="collapsed",
    )
    st.session_state.role = role
    role_desc = {
        "🙂 General User":  "Clear, balanced answers",
        "🎓 Student":       "Simple explanations + examples",
        "🔬 Researcher":    "Precise, cited responses",
        "💼 Professional":  "Actionable, concise insights",
    }
    st.caption(role_desc[role])

    st.markdown('<div class="sb-label">Document</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "PDF", type=["pdf"], label_visibility="collapsed"
    )

    vectorstore = None
    n_chunks = 0
    n_pages  = 0

    if uploaded_file:
        file_bytes = uploaded_file.read()
        with st.spinner("Indexing…"):
            vectorstore, n_chunks, n_pages = build_vectorstore(file_bytes, uploaded_file.name)

        st.markdown(f"""
        <div class="doc-card">
            <div class="doc-card-name">
                <span class="doc-ready-dot"></span>{uploaded_file.name}
            </div>
            <div class="doc-card-meta">{n_pages} pages · {n_chunks} chunks indexed</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
        if st.button("🗑 Clear conversation", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    else:
        st.markdown("""
        <div class="doc-card" style="text-align:center;padding:1rem;">
            <div style="font-size:1.5rem;margin-bottom:6px;">📄</div>
            <div style="font-size:0.78rem;color:#2D3450;">Drop a PDF above to begin</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sb-footer">
        Mistral AI · LangChain · ChromaDB
    </div>
    """, unsafe_allow_html=True)


# ── MAIN ──────────────────────────────────────────────────────────────────────
# Header
doc_name = uploaded_file.name if uploaded_file else "No document loaded"
doc_sub  = f"{n_pages} pages · {n_chunks} chunks · {role}" if uploaded_file else "Upload a PDF to start chatting"

st.markdown(f"""
<div class="page-header">
    <div class="page-header-icon">📖</div>
    <div>
        <h1>DocMind</h1>
        <div class="page-header-sub">{doc_sub}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Chat area
if not st.session_state.chat_history:
    if not uploaded_file:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">📂</div>
            <div class="empty-title">No document loaded</div>
            <div class="empty-sub">Upload a PDF from the sidebar and ask anything — DocMind will answer from it.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">💬</div>
            <div class="empty-title">Ready to answer</div>
            <div class="empty-sub">Your document is indexed. Type your first question below.</div>
        </div>
        """, unsafe_allow_html=True)
else:
    chat_html = '<div class="chat-wrap">'
    for turn in st.session_state.chat_history:
        # User bubble
        chat_html += f"""
        <div class="msg-row user">
            <div class="avatar avatar-user">👤</div>
            <div class="bubble bubble-user">
                <div class="bubble-meta meta-user">{turn["role"]}</div>
                {turn["question"]}
            </div>
        </div>"""
        # AI bubble
        sources_html = ""
        if turn["sources"]:
            chips = "".join(f'<span class="src-chip">📄 {s}</span>' for s in turn["sources"])
            sources_html = f'<div class="source-row">{chips}</div>'
        chat_html += f"""
        <div class="msg-row">
            <div class="avatar avatar-ai">🤖</div>
            <div class="bubble bubble-ai">
                <div class="bubble-meta meta-ai">DocMind</div>
                {turn["answer"]}
                {sources_html}
            </div>
        </div>"""
    chat_html += "</div>"
    st.markdown(chat_html, unsafe_allow_html=True)

# Input bar
if uploaded_file:
    st.markdown("---")
    col1, col2 = st.columns([5, 1])
    with col1:
        query = st.text_input(
            "q", placeholder="Ask anything about your document…",
            label_visibility="collapsed", key="query_input"
        )
    with col2:
        ask = st.button("Send ↑", use_container_width=True)

    if ask and query.strip():
        with st.spinner("Thinking…"):
            answer, sources = get_answer(query.strip(), vectorstore, role)
        st.session_state.chat_history.append(
            {"role": role, "question": query.strip(), "answer": answer, "sources": sources}
        )
        st.rerun()
    elif ask:
        st.warning("Please type a question first.")
