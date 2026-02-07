import streamlit as st

def main_menu():
    #menu = st.expander("Menu")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.page_link("pages/board.py", label="Přehled")
    with col2:
        st.page_link("pages/flashcard.py", label="flash card")
    with col3:
        st.page_link("pages/matching.py", label="matching")
    #with menu:
    #    tab_base, tab_company, tab_assortment, tab_settings, tab_test = st.tabs(["Přehled", "Partneři", "Sklad", "Nastavení", "Test"])
    #    with tab_base:
    #        st.page_link("pages/board.py", label="Přehled")
    #    with tab_company:
    #        st.page_link("pages/flashcard.py", label="flash card")
    #    with tab_assortment:
    #        st.write("tab_assortment")
    #    with tab_settings:
    #        st.write("tab_settings")
    #    with tab_test:
    #        st.write("tab_test")

