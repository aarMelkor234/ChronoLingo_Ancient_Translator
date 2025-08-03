import streamlit as st
import openai

import os
openai.api_key = os.getenv("OPENAI_API_KEY")

# 🏛 ChronoLingo App Settings
st.set_page_config(page_title="ChronoLingo Language Translator", layout="wide")

# Sidebar navigation
page = st.sidebar.radio("Navigate", ["ChronoLingo Translator", "Ancient Text Analyzer"])

if page == "ChronoLingo Translator":
    st.title("🕰️ ChronoLingo: Ancient Text Translator")

    language = st.selectbox(
        "Choose Ancient Language: ",
        ["Sumerian", "Ancient Greek", "Hieroglyphics"]
    )

    # Language info descriptions
    language_info = {
        "Sumerian": """Sumerian is the very first language that originated in Ancient Mesopotamia over 5000 years ago. It was used and spoken in Southern Mesopotamia beginning around 3100 BCE. As a spoken langauge, it eventually stopped being used around 2000 BCE, but it continued to be used for writing up until the first century AD. Sumerian is considered an agglutinative language, meaning that words are built by attaching a series of prefixes and suffixes to a root. Sumerian uses the SOV format for word and sentence order, which means that the subject comes first, followed by the object, and then the verb. The language played a key role in early Mesopotamian culture; it was used for everything from keeping administrative records to legal documents and even religious texts and literature. One of the most famous works in Ancient History, the Epic of Gilgamesh, was first drafted in Sumerian as literature.""",

        "Ancient Greek": """Ancient Greek was spoken from around the 9th century BCE to the 6th century CE. It featured a complex system of noun cases, verb conjugations, and moods, including the optative and aorist. It is the language of Homer, Aristotle, and the New Testament. It differs significantly from Modern Greek.""",

        "Hieroglyphics": """Hieroglyphics is a system of complex illustrations created by the Ancient Egyptians over 5000 years ago. They consisted of several illustrations such as waves, human figures, and birds combined to form a complete sentence/thought. They originated during the Pre-dynastic era around 3200 BCE and were used all the way up until the end of Roman Occupation in Egypt in the 3rd century AD. Hieroglyphs were typically carved in Egyptian temple complexes and in funerary complexes as well. The most notable of these carvings are the ones carved at the Karnak Temple Complex in Luxor. Later, Hieroglyphs developed into a verbally written system of cursive script called Hieratic. This was used only in the government as a way of managing taxes, planned buildings, and workloads."""
    }

    # Show description
    st.header(f"Current Language: {language}")
    st.subheader(f"Language Origins: {language_info[language]}")

    # 🔤 Two side-by-side columns for input and output
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Enter English Text")
        user_input = st.text_area("Input", height=300, label_visibility="collapsed")

    with col2:
        st.subheader(f"{language} Translation")
        output_placeholder = st.empty()

    # 🔁 Unified Translation Button
    if st.button(f"Translate to {language}"):
        if user_input.strip() != "":
            with st.spinner("Translating..."):
                try:
                    # 🔍 Tailored prompts per language with sample sentence
                    if language == "Sumerian":
                        prompt = f"""You are an expert in Sumerian grammar and translation. Use authentic transliteration, SOV word order, and agglutinative structure. Do not explain anything. Only return the translation.

Example:  
\"I am Aarav\" → Aarav-e me-en

Translate this to Ancient Sumerian:  
\"{user_input}\""""                       

                    elif language == "Ancient Greek":
                        prompt = f"""You are an expert in Ancient Greek grammar. Use Attic Greek with correct verb conjugation, noun cases, and diacritics. Only return the Ancient Greek translation. Do not explain anything.

Example:  
"I am Aarav" → Εῐμὶ Ἀἀραβ

Translate this to Ancient Greek:  
\"{user_input}\""""

                    elif language == "Hieroglyphics":
                        prompt = f"""You are an expert in Egyptian hieroglyphs. Return only Unicode hieroglyphs (from block U+13000–U+1342F), no transliterations or explanations.

Example:  
\"I am Aarav\" → [𓃋𓷵𒠿 𒠿𒡝𒠿𒡯]

Translate this to Egyptian Hieroglyphs:  
\"{user_input}\""""

                    response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "You are a linguistic expert specializing in ancient languages including Sumerian, Ancient Greek, and Egyptian Hieroglyphs."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.5,
                        max_tokens=500
                    )

                    translation = response["choices"][0]["message"]["content"].strip()

                    output_placeholder.text_area(
                        "Output", value=translation, height=300, label_visibility="collapsed", disabled=True
                    )

                except Exception as e:
                    output_placeholder.error(f"❌ Error: {e}")
        else:
            output_placeholder.warning("Please enter some English text to translate.")

elif page == "Ancient Text Analyzer":
    st.title("📜 Ancient Text Analyzer")
    uploaded_file = st.file_uploader("Upload Ancient Text for Analysis (.pdf, .txt, .csv)", type=["pdf", "txt", "csv"])

    if uploaded_file is not None:
        file_text = ""
        import io
        import pdfplumber

        if uploaded_file.type == "application/pdf":
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    file_text += page.extract_text() + "\n"
        else:
            file_text = uploaded_file.read().decode("utf-8")

        st.subheader("File Content Preview")
        st.text_area("Preview", file_text[:1000], height=300)

        if st.button("Analyze Historical Context"):
            with st.spinner("Analyzing historical context..."):
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "You are a historian and linguist expert in ancient texts (Greek, Sumerian, Akkadian). Provide contextual analysis, dating, cultural insight, and possible origin."},
                            {"role": "user", "content": file_text[:3000] }
                        ],
                        temperature=0.5,
                        max_tokens=700
                    )

                    st.subheader("Historical Analysis")
                    st.write(response["choices"][0]["message"]["content"].strip())

                except Exception as e:
                    st.error(f"Failed to analyze: {e}")
