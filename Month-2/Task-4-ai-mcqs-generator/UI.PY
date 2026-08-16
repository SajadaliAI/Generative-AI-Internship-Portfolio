import streamlit as st
from main import generate_mcqs, extract_text_from_pdf, generate_pdf

st.set_page_config(page_title="AI MCQs Generator", layout="wide")

# 🌟 Modern Gradient UI Theme
st.markdown("""
<style>

/* Background */
.main {
    background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
}

/* Title Styling */
h1 {
    text-align:center;
    color:#00ffff;
    font-weight:bold;
}

/* Cards */
.mcq-card {
    background: rgba(255,255,255,0.05);
    padding:20px;
    border-radius:20px;
    backdrop-filter: blur(15px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    margin-bottom:20px;
    border:1px solid rgba(255,255,255,0.1);
}

/* Buttons */
.stButton>button {
    width:100%;
    background: linear-gradient(90deg,#00c6ff,#0072ff);
    color:white;
    font-weight:bold;
    border-radius:10px;
    height:45px;
}

.stDownloadButton>button {
    width:100%;
    background: linear-gradient(90deg,#11998e,#38ef7d);
    color:white;
    border-radius:10px;
    height:45px;
}

</style>
""", unsafe_allow_html=True)

# Title
st.title("🧠 AI MCQs Generator")

st.write("Generate Question Papers using AI + LangChain + Groq")

# Inputs
topic = st.text_input("Enter Topic (Optional)")

uploaded_file = st.file_uploader("Upload PDF (Optional)", type=["pdf"])

col1, col2 = st.columns(2)

with col1:
    num = st.selectbox("Number of Questions", [5,10,15,20,25,30])

with col2:
    difficulty = st.selectbox("Difficulty", ["Easy","Medium","Hard"])

# Generate Button
if st.button("🚀 Generate Question Paper"):

    content = ""

    if uploaded_file:
        content = extract_text_from_pdf(uploaded_file)

    elif topic:
        content = topic

    else:
        st.warning("Enter Topic or Upload PDF")
        st.stop()

    with st.spinner("Generating MCQs..."):
        mcqs = generate_mcqs(content, num, difficulty)

    if mcqs:

        st.success("✅ Question Paper Ready")

        # Question Paper
        st.markdown("## 📝 Questions")

        for i, mcq in enumerate(mcqs,1):

            st.markdown(f"""
            <div class="mcq-card">
            <h3 style="color:#00ffff">Q{i}. {mcq['question']}</h3>
            """, unsafe_allow_html=True)

            for idx, option in enumerate(mcq["options"]):
                letter = chr(65+idx)
                st.markdown(f"🔹 {letter}) {option}")

            st.markdown("</div>", unsafe_allow_html=True)

        # Answer Key
        st.markdown("## ✅ Answer Key")

        for i, mcq in enumerate(mcqs,1):
            correct_letter = chr(65 + mcq["options"].index(mcq["answer"]))
            st.markdown(f"**Q{i}: {correct_letter}**")

        # PDF Download
        pdf_file = generate_pdf(mcqs)

        with open(pdf_file,"rb") as f:
            st.download_button(
                label="📥 Download Question Paper PDF",
                data=f,
                file_name="AI_MCQs_Paper.pdf",
                mime="application/pdf"
            )

    else:
        st.error("Error generating MCQs")