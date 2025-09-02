# utils.py
import streamlit as st
import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from translations import TRANSLATIONS

def initialize_session_state():
    defaults = {
        "chat_history": [],
        "app_mode": None,
        "generated_flashcards": [],
        "current_flashcard_index": 0,
        "show_definition": False,
        "flashcard_score": {"correct": 0, "total": 0},
        "selected_language": "en"  # Default to English
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def get_text(key: str, **kwargs) -> str:
    """Get translated text for the current selected language."""
    lang = st.session_state.get("selected_language", "en")
    
    if lang not in TRANSLATIONS:
        lang = "en"  # Fallback to English
    
    text = TRANSLATIONS[lang]["translations"].get(key, key)
    
    # Handle string formatting if kwargs are provided
    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError:
            # If formatting fails, return the original text
            pass
    
    return text

def get_language_flag(lang_code: str) -> str:
    """Get the flag emoji for a language code."""
    return TRANSLATIONS.get(lang_code, {}).get("flag", "🌍")

def get_language_name(lang_code: str) -> str:
    """Get the native name for a language code."""
    return TRANSLATIONS.get(lang_code, {}).get("name", lang_code)

def get_available_languages() -> dict:
    """Get all available languages with their codes, flags, and names."""
    return {
        code: {
            "flag": data["flag"],
            "name": data["name"]
        }
        for code, data in TRANSLATIONS.items()
    }

@st.cache_resource
def get_vector_db():
    DB_FOLDER_PATH = "faiss_index"

    if not os.path.exists(DB_FOLDER_PATH):
        st.error(get_text("db_folder_not_found"))
        return None

    required_files = ["index.faiss", "index.pkl"]
    missing_files = [f for f in required_files if not os.path.exists(os.path.join(DB_FOLDER_PATH, f))]

    if missing_files:
        st.error(f"📁 Missing files in '{DB_FOLDER_PATH}': {', '.join(missing_files)}")
        return None

    try:
        with st.spinner(get_text("loading_database")):
            embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            vector_db = FAISS.load_local(
                folder_path=DB_FOLDER_PATH,
                embeddings=embedding_model,
                allow_dangerous_deserialization=True
            )
        st.success(get_text("db_loaded"))
        return vector_db
    except Exception as e:
        st.error(f"Error loading vector database: {e}")
        st.info("Try regenerating the database with the PDF processing script.")
        return None