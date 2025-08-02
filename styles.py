CUSTOM_CSS = """
<style>
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        color: #f5f5dc;
    }
    
    /* Remove default padding */
    .main {
        padding-top: 1rem;
    }
    
    /* Chat messages */
    .chat-message {
        padding: 1rem 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    
    .chat-message.user {
        background: linear-gradient(135deg, #333333, #404040);
        color: #f5f5dc;
        margin-left: 2rem;
        border-left: 4px solid #f5f5dc;
    }
    
    .chat-message.assistant {
        background: linear-gradient(135deg, #f5f5dc, #ffffff);
        color: #1a1a1a;
        margin-right: 2rem;
        border-left: 4px solid #333333;
    }
    
    /* Flashcard styling */
    .flashcard {
        background: linear-gradient(135deg, #2d2d2d, #404040);
        color: #f5f5dc;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        min-height: 250px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        border: 2px solid #f5f5dc;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .flashcard:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.7);
    }
    
    .flashcard-answer {
        background: linear-gradient(135deg, #f5f5dc, #ffffff);
        color: #1a1a1a;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        min-height: 250px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        border: 2px solid #333333;
        transition: all 0.3s ease;
    }
    
    /* Score display */
    .score-display {
        background: linear-gradient(135deg, #333333, #404040);
        color: #f5f5dc;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 1rem;
        border: 1px solid #f5f5dc;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #333333, #404040);
        color: #f5f5dc;
        border: 2px solid #f5f5dc;
        border-radius: 10px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #f5f5dc, #ffffff);
        color: #1a1a1a;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(135deg, #2d2d2d, #1a1a1a);
    }
    
    /* Text input styling */
    .stTextInput > div > div > input {
        background-color: #2d2d2d;
        color: #f5f5dc;
        border: 2px solid #404040;
        border-radius: 10px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #f5f5dc;
        box-shadow: 0 0 0 2px rgba(245, 245, 220, 0.2);
    }
    
    /* Progress indicator */
    .flashcard-progress {
        background: #333333;
        color: #f5f5dc;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        text-align: center;
        margin: 1rem 0;
        border: 1px solid #f5f5dc;
    }
    
    /* Loading spinner color */
    .stSpinner > div {
        border-top-color: #f5f5dc !important;
    }
</style>
"""