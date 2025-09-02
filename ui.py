# ui.py
import streamlit as st
import services
from styles import CUSTOM_CSS
from utils import get_text, get_available_languages, get_language_flag, get_language_name

def apply_custom_css():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

def render_language_selector():
    """Render the language selector dropdown with flags."""
    languages = get_available_languages()
    
    # Create options for selectbox with flag + name
    language_options = {
        f"{data['flag']} {data['name']}": code 
        for code, data in languages.items()
    }
    
    # Get current selection for display
    current_lang = st.session_state.get("selected_language", "en")
    current_display = f"{get_language_flag(current_lang)} {get_language_name(current_lang)}"
    
    # Find the index of current language
    current_index = list(language_options.keys()).index(current_display) if current_display in language_options else 0
    
    selected_display = st.selectbox(
        get_text("language"),
        options=list(language_options.keys()),
        index=current_index,
        key="language_selector"
    )
    
    # Update session state if selection changed
    new_lang_code = language_options[selected_display]
    if new_lang_code != st.session_state.get("selected_language"):
        st.session_state.selected_language = new_lang_code
        st.rerun()

def sidebar_info():
    with st.sidebar:
        # Language selector at the top of sidebar
        render_language_selector()
        
        st.divider()
        
        # Check if image exists, if not just show text
        try:
            st.image("boundless.jpg", use_column_width=True)
        except:
            st.info("Place 'boundless.jpg' in your project folder for the logo")
        
        st.markdown(f"## {get_text('app_title')}")
        st.markdown("*Universal ZK Protocol Learning Tool*")

        # Display flashcard score if available
        if st.session_state.flashcard_score["total"] > 0:
            score = st.session_state.flashcard_score
            percentage = round((score["correct"] / score["total"]) * 100)
            st.markdown(f"### {get_text('learning_progress')}")
            st.markdown(f"""
            <div class="score-display">
                <strong>{get_text('score')}: {score["correct"]}/{score["total"]}</strong><br>
                <strong>{get_text('accuracy')}: {percentage}%</strong>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"### {get_text('quick_actions')}")
        if st.button(get_text("reset_chat"), use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

        if st.button(get_text("reset_score"), use_container_width=True):
            st.session_state.flashcard_score = {"correct": 0, "total": 0}
            st.rerun()

def chat_interface(db):
    st.markdown(f"## {get_text('chat_assistant')}")
    st.markdown(f"*{get_text('ask_anything')}*")

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input(get_text("ask_about_boundless")):
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate and display response
        with st.chat_message("assistant"):
            response = services.generate_rag_response(prompt, db)
            st.markdown(response)

        st.session_state.chat_history.append({"role": "assistant", "content": response})

def flashcard_interface(db):
    st.markdown(f"## {get_text('knowledge_flashcards')}")
    st.markdown(f"*{get_text('test_knowledge')}*")

    # Score display
    score = st.session_state.flashcard_score
    if score["total"] > 0:
        percentage = round((score["correct"] / score["total"]) * 100)
        st.markdown(f"""
        <div class="score-display">
            <h3>{get_text('your_progress')}</h3>
            <h2>{score["correct"]}/{score["total"]} {get_text('score').lower()} ({percentage}%)</h2>
        </div>
        """, unsafe_allow_html=True)

    # Generate new flashcards button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(get_text("generate_new_flashcards"), use_container_width=True, type="primary"):
            with st.spinner(get_text("creating_flashcards")):
                st.session_state.generated_flashcards = services.generate_flashcards(db, 5)
                st.session_state.current_flashcard_index = 0
                st.session_state.show_definition = False
                if st.session_state.generated_flashcards:
                    st.success(get_text("flashcards_generated", count=len(st.session_state.generated_flashcards)))
                st.rerun()

    # Display flashcards
    flashcards = st.session_state.generated_flashcards
    
    if flashcards:
        current_index = st.session_state.current_flashcard_index
        current_card = flashcards[current_index]

        # Progress indicator
        st.markdown(f"""
        <div class="flashcard-progress">
            {get_text("flashcard_count", current=current_index + 1, total=len(flashcards))}
        </div>
        """, unsafe_allow_html=True)

        # Flashcard display
        if not st.session_state.show_definition:
            st.markdown(f"""
            <div class="flashcard">
                <div>
                    <h2>{get_text("question")}</h2>
                    <h3>{current_card["question"]}</h3>
                </div>
            </div>
            """, unsafe_allow_html=True)

            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button(get_text("show_answer"), use_container_width=True):
                    st.session_state.show_definition = True
                    st.rerun()
        else:
            st.markdown(f"""
            <div class="flashcard-answer">
                <div>
                    <h2>{get_text("answer")}</h2>
                    <p>{current_card["answer"]}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(get_text("how_did_you_do"))
            col1, col2 = st.columns(2)

            def handle_next_card(correct):
                if correct:
                    st.session_state.flashcard_score["correct"] += 1
                st.session_state.flashcard_score["total"] += 1
                
                if current_index < len(flashcards) - 1:
                    st.session_state.current_flashcard_index += 1
                    st.session_state.show_definition = False
                else:
                    st.info(get_text("completed_flashcards"))
                
                # We need to rerun to reflect the changes
                if correct:
                    st.success(get_text("great_job"))
                else:
                    st.info(get_text("keep_learning"))
                st.rerun()

            if col1.button(get_text("got_it_right"), type="primary", use_container_width=True):
                handle_next_card(correct=True)

            if col2.button(get_text("need_more_practice"), use_container_width=True):
                handle_next_card(correct=False)

        # Navigation buttons
        if len(flashcards) > 1:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                if st.button(get_text("previous"), disabled=current_index == 0):
                    st.session_state.current_flashcard_index -= 1
                    st.session_state.show_definition = False
                    st.rerun()
            with col3:
                if st.button(get_text("next"), disabled=current_index == len(flashcards) - 1):
                    st.session_state.current_flashcard_index += 1
                    st.session_state.show_definition = False
                    st.rerun()
    else:
        st.markdown(f"""
        <div class="flashcard">
            <div>
                <h2>{get_text("ready_to_test")}</h2>
                <p>{get_text("click_generate")}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_mode_selection():
    st.markdown(f"## {get_text('choose_learning_mode')}")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        ### {get_text('interactive_chat')}
        {get_text('chat_description')}
        """)
        if st.button(get_text("start_chatting"), use_container_width=True, type="primary"):
            st.session_state.app_mode = 'chat'
            st.rerun()
    with col2:
        st.markdown(f"""
        ### {get_text('knowledge_flashcards')}
        {get_text('flashcard_description')}
        """)
        if st.button(get_text("generate_flashcards"), use_container_width=True, type="secondary"):
            st.session_state.app_mode = 'flashcards'
            st.rerun()