import streamlit as st

def main_menu():
    """
    Create main menu
    """
    col1, col2, col3, col4, col5 = st.columns([13,13,13,13,17])
    with col1:
        st.page_link("pages/board.py", label="Přehled")
    with col2:
        st.page_link("pages/flashcard.py", label="Flash card")
    with col3:
        st.page_link("pages/matching.py", label="Matching")
    with col4:
        st.page_link("pages/storytelling.py", label="Story Telling")
    with col5:
        st.page_link("pages/sentence_changer.py", label="Sentence Changer")
