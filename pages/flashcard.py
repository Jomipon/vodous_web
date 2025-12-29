"""
First game
Do you known translate for random word ?
"""
import os
import json
import streamlit as st
from dotenv import load_dotenv
from support import download_get_url

def parse_responce_new_word(responce):
    """
    Create answer from sql data
    """
    return {
        "orig_word_id":responce["data"]["word_id_from"],
        "orig_word": responce["data"]["word_content_from"],
        "orig_language": responce["data"]["word_language_from"],
        "orig_note": responce["data"]["note_from"],
        "tran_word_id":responce["data"]["word_id_to"],
        "tran_word": responce["data"]["word_content_to"],
        "tran_language": responce["data"]["word_language_to"],
        "tran_note": responce["data"]["note_to"],
        "random_id": responce["data"]["random_id"]
            }

def find_new_word():
    """
    Send request to API for next word
    """
    url_base = os.getenv("FAST_API_URL_BASE")
    url_random_word = os.getenv("FAST_API_URL_RANDOM_WORD")
    url = url_base + url_random_word.format(id_seed=123456789)
    random_word = download_get_url(url)
    if random_word["status"] == 200:
        new_word = parse_responce_new_word(json.loads(random_word["data"]))
    else:
        new_word = ""
    st.session_state["word_original"] = new_word

def reset_word():
    """
    Reset values to reload word
    """
    st.session_state.reset = True

def main():
    """
    Main method for flashcard
    """
    load_dotenv()

    if st.session_state.get("reset", True):
        find_new_word()
        st.session_state.reset = False
    st.markdown("<h2><b>Flashcard</b></h2>",unsafe_allow_html=True)
    if st.session_state["word_original"]:
        with st.form("word_chosser", clear_on_submit=True):
            st.markdown(f"<h3><b>{st.session_state["word_original"]["orig_word"]}</b></h3>",unsafe_allow_html=True)
            st.markdown(f"<i>{st.session_state["word_original"]["orig_note"]}</i>",unsafe_allow_html=True)
            if st.form_submit_button("Přeložit"):
                st.markdown(f"<h3><b>{st.session_state["word_original"]["tran_word"]}</b></h3>",unsafe_allow_html=True)
                st.markdown(f"<i>{st.session_state["word_original"]["tran_note"]}</i>",unsafe_allow_html=True)
                st.form_submit_button("Další", on_click=reset_word)
    else:
        st.write("Chyba při připojení na server")
if __name__ == "__main__":
    main()
