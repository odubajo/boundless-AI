🚀 Boundless AI Assistant
An interactive AI assistant built with Streamlit and the Google Gemini API to provide information and a learning tool for the Boundless protocol. This application demonstrates Retrieval-Augmented Generation (RAG) by querying a local vector database of Boundless documentation to provide accurate, context-aware answers.

✨ Features
Interactive Chat: Ask questions about the Boundless protocol and receive detailed answers based on the provided documentation.

Knowledge Flashcards: Generate a set of personalized flashcards to test your knowledge of key concepts.

Retrieval-Augmented Generation (RAG): The core logic retrieves relevant information from a vector database before generating a response, ensuring high accuracy.

Modular Codebase: The code is organized into separate files for a clean, maintainable, and scalable project structure.

Secure API Handling: Your Google Gemini API key is securely stored in a .env file, separate from the codebase.

⚙️ Prerequisites
Before running the application, ensure you have the following installed:

Python 3.8+

pip (Python package installer)

A Google Gemini API Key

The faiss_index directory containing your pre-processed document embeddings.

📦 Installation
Clone the Repository (or create the files):
First, create the four Python files (app.py, config.py, rag_logic.py, ui_components.py) and place them in a single directory.

Install Required Libraries:
Open your terminal or command prompt and navigate to the project directory. Run the following command to install all necessary Python libraries:

pip install streamlit langchain_community numpy requests python-dotenv
pip install "faiss-cpu>=1.7.0"

Set up the Vector Database:
You need to have a faiss_index directory in your project folder. This directory should contain the index.faiss and index.pkl files generated from the Boundless documentation.

Configure your API Key:
Create a file named .env in the root of your project directory. Inside this file, add your Google Gemini API key as follows:

API_KEY="YOUR_API_KEY_HERE"

Note: Replace "YOUR_API_KEY_HERE" with your actual API key.

▶️ Usage
To run the application, simply execute the following command in your terminal from the project's root directory:

streamlit run app.py
