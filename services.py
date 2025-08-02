import streamlit as st
import json
import random
from api_client import call_gemini_api

def generate_rag_response(user_query: str, db) -> str:
    if db is None:
        return "Knowledge base is not available."

    try:
        with st.spinner("Searching knowledge base..."):
            relevant_docs = db.similarity_search(user_query, k=4) 

        if not relevant_docs:
            return "🤔 I couldn't find relevant information in my knowledge base for that question."

        context = "\n\n".join([f"Document {i+1}:\n{doc.page_content}"
                              for i, doc in enumerate(relevant_docs)])

        prompt = f"""You are a knowledgeable AI assistant specializing in Boundless and RISC Zero's ZK Protocol. 
        
Using the context below, provide a helpful and accurate answer to the user's question. 
If the context doesn't contain enough information, acknowledge this and provide what information you can.

Context:
{context}

User Question: {user_query}

Please provide a clear, informative answer:"""

        with st.spinner("🤖 Generating response..."):
            return call_gemini_api(prompt)

    except Exception as e:
        return f"An error occurred while processing your question: {e}"

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

        prompt = f"""Create {num_flashcards} educational flashcards about Boundless and RISC Zero's ZK Protocol based on the provided context.

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

        with st.spinner("🎴 Generating flashcards..."):
            response = call_gemini_api(prompt, use_json_schema=True, schema=schema)

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            st.error("Failed to parse flashcard response.")
            return []

    except Exception as e:
        st.error(f"Error generating flashcards: {e}")
        return []