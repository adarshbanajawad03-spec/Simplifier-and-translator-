import streamlit as st

from utils.extractor import extract_text_from_file
from utils.ocr_utils import extract_text_from_image
from utils.llm_utils import simplify_text

from utils.translator_utils import (
    detect_language,
    translate_text_free,
    )
from utils.translator_utils import (
    detect_language,
    translate_text_free,
    )
from utils.export_utils import (
    generate_txt_file,
    generate_docx_file,
    )
from utils.helpers import (
    chunk_text,
    parse_glossary,
    calculate_readability_score,
    )

st.set_page_config(
    page_title="Text Simplifier & Translator",
    layout="wide",
    )

st.title("📘 Text Simplifier & Translator")

st.markdown(
    """
Simplify complex documents into plain language and translate them across multiple languages.
Supports PDFs, DOCX, TXT, and OCR image extraction.
"""
)

SUPPORTED_IMAGE_TYPES = ["png", "jpg", "jpeg"]

LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Kannada": "kn",
    "Tamil": "ta",
    "Telugu": "te",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Bengali": "bn",
    "Urdu": "ur",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Chinese": "zh-cn",
    "Japanese": "ja",
    "Korean": "ko",
    "Arabic": "ar",
}

if "history" not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    st.header("⚙ Configuration")

    input_mode = st.radio(
        "Input Mode",
        ["Paste Text", "Upload File"]
    )

    operation_type = st.selectbox(
        "Operation Type",
        [
            "Simplify Only",
            "Translate Only",
            "Simplify Then Translate",
        ],
    )

    simplification_level = st.selectbox(
        "Simplification Level",
        [
            "Beginner",
            "Student",
            "General Public",
            "Professional Summary",
        ],
    )

    target_language = st.selectbox(
        "Target Language",
        list(LANGUAGES.keys()),
    )

    glossary_text = st.text_area(
        "Glossary Terms",
        placeholder="AI = Artificial Intelligence",
        height=150,
    )

uploaded_file = None
raw_text = ""

if input_mode == "Paste Text":
    raw_text = st.text_area(
        "Paste Text",
        height=300,
        placeholder="Paste your text here...",
    )

else:
    uploaded_file = st.file_uploader(
        "Upload File",
        type=["pdf", "docx", "txt", "png", "jpg", "jpeg"],
    )

if uploaded_file:
    try:
        extension = uploaded_file.name.split(".")[-1].lower()

        if extension in SUPPORTED_IMAGE_TYPES:
            raw_text = extract_text_from_image(uploaded_file)

        else:
            raw_text = extract_text_from_file(uploaded_file)

        st.success("File processed successfully.")

    except Exception as e:
        st.error(f"File processing failed: {e}")

process_button = st.button("🚀 Process")

if process_button:

    if not raw_text.strip():
        st.error("Please provide text or upload a file.")
        st.stop()

    glossary = parse_glossary(glossary_text)

    try:
        with st.spinner("Processing..."):

            detected_language = detect_language(raw_text)

            chunks = chunk_text(raw_text, max_chars=3500)

            simplified_chunks = []
            translated_chunks = []

            for chunk in chunks:

                simplified_output = chunk
                translated_output = chunk

                if operation_type in [
                    "Simplify Only",
                    "Simplify Then Translate",
                ]:

                    simplified_output = simplify_text(
                        text=chunk,
                        level=simplification_level,
                        glossary=glossary,
                    )

                if operation_type == "Translate Only":

                    translated_output = translate_text_free(
                        text=chunk,
                        target_language=target_language,
                    )

                elif operation_type == "Simplify Then Translate":

                    translated_output = translate_text_free(
                        text=simplified_output,
                        target_language=target_language,
                    )

                simplified_chunks.append(simplified_output)
                translated_chunks.append(translated_output)

            simplified_text = "\n".join(simplified_chunks)
            translated_text = "\n".join(translated_chunks)

            before_score = calculate_readability_score(raw_text)
            after_score = calculate_readability_score(
                simplified_text
            )

            st.success("Processing completed successfully.")

            st.warning(
                "Human review recommended for legal, medical, or technical content."
            )

            st.subheader("📊 Readability Scores")

            col_a, col_b = st.columns(2)

            with col_a:
                st.metric(
                    "Original Text",
                    before_score,
                )

            with col_b:
                st.metric(
                    "Simplified Text",
                    after_score,
                )

            st.subheader("🌐 Detected Language")
            st.info(detected_language)

            col1, col2, col3 = st.columns(3)

            with col1:
                st.subheader("Original Text")

                original_box = st.text_area(
                    "Original",
                    raw_text,
                    height=400,
                )

            with col2:
                st.subheader("Simplified Text")

                simplified_box = st.text_area(
                    "Simplified",
                    simplified_text,
                    height=400,
                )

            with col3:
                st.subheader("Translated Text")

                translated_box = st.text_area(
                    "Translated",
                    translated_text,
                    height=400,
                )

            final_output = f"""
Original Text:

{original_box}

Simplified Text:

{simplified_box}

Translated Text:

{translated_box}
"""

            txt_data = generate_txt_file(final_output)
            docx_data = generate_docx_file(final_output)

            st.subheader("📥 Download")

            col_d1, col_d2 = st.columns(2)

            with col_d1:
                st.download_button(
                    label="Download TXT",
                    data=txt_data,
                    file_name="output.txt",
                    mime="text/plain",
                )

            with col_d2:
                st.download_button(
                    label="Download DOCX",
                    data=docx_data,
                    file_name="output.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )

            st.session_state.history.append(
                {
                    "language": detected_language,
                    "operation": operation_type,
                }
            )

            st.subheader("📜 History")

            for item in st.session_state.history[-5:]:
                st.write(item)

    except Exception as e:
        st.error(f"Processing failed: {e}")