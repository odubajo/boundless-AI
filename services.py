# services.py
import streamlit as st
import json
import random
from api_client import call_gemini_api
from utils import get_text, get_language_name

def generate_rag_response(user_query: str, db) -> str:
    if db is None:
        return get_text("db_not_available")

    try:
        with st.spinner(get_text("searching_knowledge")):
            relevant_docs = db.similarity_search(user_query, k=4) 

        if not relevant_docs:
            return get_text("no_relevant_info")

        context = "\n\n".join([f"Document {i+1}:\n{doc.page_content}"
                              for i, doc in enumerate(relevant_docs)])

        # Get the current language for response
        current_lang = st.session_state.get("selected_language", "en")
        lang_name = get_language_name(current_lang)
        
        # Create language-specific prompt
        language_instruction = ""
        if current_lang != "en":
            language_instruction = f"Please respond in {lang_name}. "

        prompt = f"""You are a knowledgeable AI assistant specializing in Boundless and RISC Zero's ZK Protocol. 
        
{language_instruction}Using the context below, provide a helpful and accurate answer to the user's question. 
If the context doesn't contain enough information, acknowledge this and provide what information you can.

Context:
{context}

User Question: {user_query}

Please provide a clear, informative answer:"""

        with st.spinner(get_text("generating_response")):
            return call_gemini_api(prompt)

    except Exception as e:
        return get_text("error_processing", error=str(e))

def generate_flashcards(db, num_flashcards: int = 5) -> list:
    if db is None:
        return []

    try:
        all_docs = list(db.docstore._dict.values())

        if len(all_docs) < num_flashcards:
            selected_docs = all_docs
            num_flashcards = len(all_docs)
        else:
            selected_docs = random.sample(all_docs, num_flashcards * 2)  # Get more docs for variety

        # Create context from selected documents
        context = "\n\n---DOCUMENT SEPARATOR---\n\n".join([doc.page_content for doc in selected_docs])

        # Get the current language for flashcards
        current_lang = st.session_state.get("selected_language", "en")
        lang_name = get_language_name(current_lang)
        
        # Create language-specific prompt
        language_instruction = ""
        if current_lang != "en":
            language_instruction = f"Create the flashcards in {lang_name}. Both questions and answers should be in {lang_name}. "

        prompt = f"""{language_instruction}Create {num_flashcards} educational flashcards about Boundless and RISC Zero's ZK Protocol based on the provided context.

Each flashcard should:
- Have a clear, specific question
- Include a comprehensive answer
- Focus on key concepts, technical details, or important facts
- Be suitable for testing knowledge about the protocol

Context:
{context}

Generate exactly {num_flashcards} flashcards in the specified JSON format."""

        schema = {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "question": {"type": "STRING"},
                    "answer": {"type": "STRING"}
                },
                "required": ["question", "answer"]
            }
        }

        with st.spinner(get_text("generating_flashcards")):
            response = call_gemini_api(prompt, use_json_schema=True, schema=schema)

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            st.error("Failed to parse flashcard response.")
            return []

    except Exception as e:
        st.error(f"Error generating flashcards: {e}")
        return []