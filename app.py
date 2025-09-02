# app.py
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

    # Render header and sidebar with language support
    st.markdown(f"# {utils.get_text('community_knowledge')}")
    st.markdown(f"*{utils.get_text('app_subtitle')}*")
    ui.sidebar_info()

    db = utils.get_vector_db()
    if not db:
        st.error(utils.get_text("cannot_proceed"))
        st.stop()

    if st.session_state.app_mode is None:
        ui.render_mode_selection()
    else:
        if st.button(utils.get_text("back_to_menu"), type="secondary"):
            st.session_state.app_mode = None
            st.rerun()

        if st.session_state.app_mode == 'chat':
            ui.chat_interface(db)
        elif st.session_state.app_mode == 'flashcards':
            ui.flashcard_interface(db)

if __name__ == "__main__":
    main()