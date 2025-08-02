# main.py
import streamlit as st
import utils
import ui

def main():
    """Main application flow"""
    # Configure the Streamlit page
    st.set_page_config(
        page_title="Boundless AI Assistant",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Prepare the app by initializing state and applying styles
    utils.initialize_session_state()
    ui.apply_custom_css()

    # Render header and sidebar
    st.markdown("# 🚀 Boundless communtity knowledge assistant")
    st.markdown("*Learn about RISC Zero's Universal ZK Protocol*")
    ui.sidebar_info()

    db = utils.get_vector_db()
    if not db:
        st.error("❌ Cannot proceed without vector database. Please check the setup instructions.")
        st.stop()

    if st.session_state.app_mode is None:
        ui.render_mode_selection()
    else:
        if st.button("⬅ Back to Menu", type="secondary"):
            st.session_state.app_mode = None
            st.rerun()

        if st.session_state.app_mode == 'chat':
            ui.chat_interface(db)
        elif st.session_state.app_mode == 'flashcards':
            ui.flashcard_interface(db)

if __name__ == "__main__":
    main()