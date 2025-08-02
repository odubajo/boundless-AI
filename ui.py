import streamlit as st
import services
from styles import CUSTOM_CSS

def apply_custom_css():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

def sidebar_info():
    with st.sidebar:
        st.image("boundless.jpg", use_column_width=True)
        st.markdown("## 🚀 Boundless AI Assistant")
        st.markdown("*Universal ZK Protocol Learning Tool*")

        # Display flashcard score if available
        if st.session_state.flashcard_score["total"] > 0:
            score = st.session_state.flashcard_score
            percentage = round((score["correct"] / score["total"]) * 100)
            st.markdown("### 📊 Learning Progress")
            st.markdown(f"""
            <div class="score-display">
                <strong>Score: {score["correct"]}/{score["total"]}</strong><br>
                <strong>Accuracy: {percentage}%</strong>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("### 🛠️ Quick Actions")
        if st.button("🔄 Reset Chat History", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

        if st.button("📈 Reset Flashcard Score", use_container_width=True):
            st.session_state.flashcard_score = {"correct": 0, "total": 0}
            st.rerun()

def chat_interface(db):
    st.markdown("## 💬 Chat Assistant")
    st.markdown("*GBERRY beleiver Ask me anything about Boundless and RISC Zero's ZK Protocol*")

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask me about Boundless..."):
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
    st.markdown("## 🎴 Knowledge Flashcards")
    st.markdown("*GBERRY beleiver Test your knowledge about boundless*")

    # Score display
    score = st.session_state.flashcard_score
    if score["total"] > 0:
        percentage = round((score["correct"] / score["total"]) * 100)
        st.markdown(f"""
        <div class="score-display">
            <h3>📊 Your Progress</h3>
            <h2>{score["correct"]}/{score["total"]} correct ({percentage}%)</h2>
        </div>
        """, unsafe_allow_html=True)

    # Generate new flashcards button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎲 Generate New Flashcards", use_container_width=True, type="primary"):
            with st.spinner("Creating personalized flashcards..."):
                st.session_state.generated_flashcards = services.generate_flashcards(db, 5)
                st.session_state.current_flashcard_index = 0
                st.session_state.show_definition = False
                if st.session_state.generated_flashcards:
                    st.success(f"✅ Generated {len(st.session_state.generated_flashcards)} flashcards!")
                st.rerun()

    # Display flashcards
    flashcards = st.session_state.generated_flashcards
    
    if flashcards:
        current_index = st.session_state.current_flashcard_index
        current_card = flashcards[current_index]

        # Progress indicator
        st.markdown(f"""
        <div class="flashcard-progress">
            Flashcard {current_index + 1} of {len(flashcards)}
        </div>
        """, unsafe_allow_html=True)

        # Flashcard display
        if not st.session_state.show_definition:
            st.markdown(f"""
            <div class="flashcard">
                <div>
                    <h2>❓ Question</h2>
                    <h3>{current_card["question"]}</h3>
                </div>
            </div>
            """, unsafe_allow_html=True)

            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🔄 Show Answer", use_container_width=True):
                    st.session_state.show_definition = True
                    st.rerun()
        else:
            st.markdown(f"""
            <div class="flashcard-answer">
                <div>
                    <h2>✅ Answer</h2>
                    <p>{current_card["answer"]}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("**How did you do?**")
            col1, col2 = st.columns(2)

            def handle_next_card(correct):
                if correct:
                    st.session_state.flashcard_score["correct"] += 1
                st.session_state.flashcard_score["total"] += 1
                
                if current_index < len(flashcards) - 1:
                    st.session_state.current_flashcard_index += 1
                    st.session_state.show_definition = False
                else:
                    st.info("🎊 You've completed all flashcards! Generate new ones to continue.")
                
                # We need to rerun to reflect the changes
                if correct:
                    st.success("Great job! 🎉")
                else:
                    st.info("Keep learning! 📚")
                st.rerun()

            if col1.button("✅ Got it right!", type="primary", use_container_width=True):
                handle_next_card(correct=True)

            if col2.button("❌ Need more practice", use_container_width=True):
                handle_next_card(correct=False)


        # Navigation buttons
        if len(flashcards) > 1:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                if st.button("◀ Previous", disabled=current_index == 0):
                    st.session_state.current_flashcard_index -= 1
                    st.session_state.show_definition = False
                    st.rerun()
            with col3:
                if st.button("Next ▶", disabled=current_index == len(flashcards) - 1):
                    st.session_state.current_flashcard_index += 1
                    st.session_state.show_definition = False
                    st.rerun()
    else:
        st.markdown("""
        <div class="flashcard">
            <div>
                <h2>🚀 Ready to test your knowledge?</h2>
                <p>Click "Generate New Flashcards" to create personalized questions based on the Boundless documentation!</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_mode_selection():
    st.markdown("## 🎯 GBERRY beleiver Choose Your Learning Mode")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### 💬 Interactive Chat
        Ask questions and get detailed answers about Boundless protocol.
        """)
        if st.button("Start Chatting", use_container_width=True, type="primary"):
            st.session_state.app_mode = 'chat'
            st.rerun()
    with col2:
        st.markdown("""
        ### 🎴 Knowledge Flashcards  
        Test your understanding with flashcards and track your progress.
        """)
        if st.button("Generate Flashcards", use_container_width=True, type="secondary"):
            st.session_state.app_mode = 'flashcards'
            st.rerun()