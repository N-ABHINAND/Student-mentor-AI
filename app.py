# ============================================
# AI PERSONAL STUDY MENTOR
# FULL FINAL VERSION WITH DOWNLOADS
# ============================================

from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import fitz
from groq import Groq

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="Back Bencher AI",
    page_icon="🎓",
    layout="wide"
)

# ============================================
# GROQ API SETUP
# ============================================

import os

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL_NAME = "llama-3.3-70b-versatile"

# ============================================
# SESSION STORAGE
# ============================================

if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

# ============================================
# LANGUAGE FUNCTION
# ============================================

def get_language_instruction(language):

    if language == "Tamil":

        return """
        Answer only in Tamil language.
        """

    elif language == "Tanglish":

        return """
        Answer only in Tanglish.

        Use English letters but Tamil speaking style.

        Example:
        'Machine learning na data use panni learn panrathu.'
        """

    else:

        return """
        Answer only in English language.
        """

# ============================================
# GENERATE RESPONSE
# ============================================

def generate_response(prompt):

    completion = client.chat.completions.create(

        model=MODEL_NAME,

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.5
    )

    return completion.choices[0].message.content

# ============================================
# PDF EXTRACTION
# ============================================

def extract_pdf_text(uploaded_file):

    text = ""

    pdf_document = fitz.open(
        stream=uploaded_file.read(),
        filetype="pdf"
    )

    for page in pdf_document:

        text += page.get_text()

    return text

# ============================================
# CHATBOT RESPONSE
# ============================================

def chatbot_response(question, language):

    instruction = get_language_instruction(language)

    prompt = f"""
    {instruction}

    You are an AI Personal Study Mentor.

    Explain concepts clearly for students.

    Strictly answer using the uploaded PDF content.

    If the answer is unavailable in the PDF,
    say:
    "This information is not available in uploaded syllabus."

    Uploaded PDF Content:
    {st.session_state.pdf_text[:12000]}

    Student Question:
    {question}
    """

    return generate_response(prompt)

# ============================================
# SUMMARY
# ============================================

def summarize_pdf(language):

    instruction = get_language_instruction(language)

    prompt = f"""
    {instruction}

    Summarize the uploaded syllabus.

    Give:
    1. Important Topics
    2. Key Concepts
    3. Important Units
    4. Exam Preparation Tips

    Content:
    {st.session_state.pdf_text[:12000]}
    """

    return generate_response(prompt)

# ============================================
# QUIZ GENERATOR
# ============================================

def generate_quiz(language):

    instruction = get_language_instruction(language)

    prompt = f"""
    {instruction}

    Generate 5 important quiz questions
    from the uploaded syllabus.

    Content:
    {st.session_state.pdf_text[:12000]}
    """

    return generate_response(prompt)

# ============================================
# STUDY PLAN
# ============================================

def generate_study_plan(language):

    instruction = get_language_instruction(language)

    prompt = f"""
    {instruction}

    Create a smart study plan.

    Divide topics day-wise.

    Content:
    {st.session_state.pdf_text[:12000]}
    """

    return generate_response(prompt)

# ============================================
# SIDEBAR
# ============================================

st.sidebar.title("⚙ Settings")

language = st.sidebar.selectbox(
    "Select Language",
    ["English", "Tamil", "Tanglish"]
)

st.sidebar.markdown("---")

st.sidebar.info(
    """
    ✅ PDF Summary

    ✅ Quiz Generator

    ✅ Study Planner

    ✅ AI Learning Chatbot

    ✅ Multilingual Support

    ✅ Download Notes
    """
)

# ============================================
# MAIN TITLE
# ============================================

st.title("🎓 Back Bencher AI")

st.markdown(
    "### Multilingual AI Tutor"
)

# ============================================
# PDF UPLOAD
# ============================================

uploaded_file = st.file_uploader(
    "📄 Upload Syllabus PDF",
    type=["pdf"]
)

# ============================================
# MAIN WORKFLOW
# ============================================

if uploaded_file is not None:

    with st.spinner("Reading PDF..."):

        text = extract_pdf_text(uploaded_file)

        st.session_state.pdf_text = text

    st.success("✅ PDF Uploaded Successfully!")

    st.toast("📘 Syllabus Ready!")

    # ========================================
    # CHATBOT SECTION
    # ========================================

    st.divider()

    st.subheader("💬 AI Learning Chatbot")

    st.markdown(
        "Ask anything from the uploaded syllabus."
    )

    # Show Previous Messages
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    # User Input
    user_question = st.chat_input(
        "Ask your doubt here..."
    )

    # Generate AI Response
    if user_question:

        # Save User Message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_question
            }
        )

        # Show User Message
        with st.chat_message("user"):

            st.markdown(user_question)

        # AI Response
        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                answer = chatbot_response(
                    user_question,
                    language
                )

                st.markdown(answer)

        # Save AI Response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

    # ========================================
    # DOWNLOAD CHAT HISTORY
    # ========================================

    st.divider()

    chat_text = ""

    for message in st.session_state.messages:

        role = message["role"]
        content = message["content"]

        chat_text += f"{role.upper()}:\n{content}\n\n"

    st.download_button(
        label="⬇ Download Chat History",
        data=chat_text,
        file_name="chat_history.txt",
        mime="text/plain"
    )

    # ========================================
    # SUMMARY SECTION
    # ========================================

    st.divider()

    st.subheader("📘 PDF Summary")

    if st.button("Generate Summary"):

        with st.spinner("Generating Summary..."):

            summary = summarize_pdf(language)

        st.toast("✅ Summary Generated!")

        st.write(summary)

        st.download_button(
            label="⬇ Download Summary",
            data=summary,
            file_name="summary.txt",
            mime="text/plain"
        )

    # ========================================
    # QUIZ SECTION
    # ========================================

    st.divider()

    st.subheader("🧠 Quiz Generator")

    if st.button("Generate Quiz"):

        with st.spinner("Generating Quiz..."):

            quiz = generate_quiz(language)

        st.toast("✅ Quiz Generated!")

        st.write(quiz)

        st.download_button(
            label="⬇ Download Quiz",
            data=quiz,
            file_name="quiz.txt",
            mime="text/plain"
        )

    # ========================================
    # STUDY PLAN SECTION
    # ========================================

    st.divider()

    st.subheader("📅 Study Plan")

    if st.button("Generate Study Plan"):

        with st.spinner("Generating Study Plan..."):

            plan = generate_study_plan(language)

        st.toast("✅ Study Plan Generated!")

        st.write(plan)

        st.download_button(
            label="⬇ Download Study Plan",
            data=plan,
            file_name="study_plan.txt",
            mime="text/plain"
        )

else:

    st.info("📄 Upload a PDF to begin.")

# ============================================
# FOOTER
# ============================================

st.divider()

st.caption(
    "🚀 Built using Streamlit + Groq API + Agentic AI"
)