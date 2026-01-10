"""
First game
Do you known translate for random word ?
"""
import os
import json
import streamlit as st
from dotenv import load_dotenv
import plotly.graph_objects as go
from support import download_get_url, download_post_url

def parse_responce_new_word(responce):
    """
    Create answer from sql data
    """
    return {
        "orig_word_id":responce["data"]["word_id_from"],
        "orig_word": responce["data"]["word_content_from"],
        "orig_language": responce["data"]["word_language_from"],
        "orig_note": responce["data"]["note_from"],
        "tran_id":responce["data"]["word_translate_id"],
        "tran_word_id":responce["data"]["word_id_to"],
        "tran_word": responce["data"]["word_content_to"],
        "tran_language": responce["data"]["word_language_to"],
        "tran_note": responce["data"]["note_to"],
        "random_id": responce["data"]["random_id"],
        "success_rate": responce["data"]["translate_success_rate"]
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

def get_word_speech(word_id):
    """
    Download speech for word
    """
    if not st.session_state.get("word_speech", None):
        url_base = os.getenv("FAST_API_URL_BASE")
        url_word_speech = os.getenv("FAST_API_URL_WORD_SPEECH")
        url = url_base + url_word_speech.format(word_id=word_id)
        speech_word = download_get_url(url)

        st.session_state["word_speech"] = speech_word

def set_rating(word_translate_id: str, rating: float):
    """
    Set rating for this translate
    
    :param word_translate_id: Translate ID
    :type word_translate_id: str
    :param rating: Rating
    :type rating: float
    """
    url_base = os.getenv("FAST_API_URL_BASE")
    url_rating_word = os.getenv("FAST_API_URL_WORD_RATING")
    url = url_base + url_rating_word.format(word_translate_id = word_translate_id, rating = rating)
    download_post_url(url, "()", [])
    reset_word()
    
def reset_word():
    """
    Reset values to reload word
    """
    st.session_state.reset = True
    st.session_state["word_speech"] = None

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
            if st.form_submit_button("", icon=":material/speaker:"):
                get_word_speech(st.session_state["word_original"]["orig_word_id"])
                audio = st.session_state["word_speech"]
                st.audio(audio["data"], format="audio/mp3", autoplay=True)
            if st.form_submit_button("Přeložit"):
                st.markdown(f"<h3><b>{st.session_state["word_original"]["tran_word"]}</b></h3>",unsafe_allow_html=True)
                st.markdown(f"<i>{st.session_state["word_original"]["tran_note"]}</i>",unsafe_allow_html=True)
                score = st.session_state["word_original"]["success_rate"]
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.form_submit_button("Věděl jsem", on_click=set_rating, args=(st.session_state["word_original"]["tran_id"], 1.0,))
                with col2:
                    st.form_submit_button("Částečně", on_click=set_rating, args=(st.session_state["word_original"]["tran_id"], 0.5,))
                with col3:
                    st.form_submit_button("Nevěděl jsem", on_click=set_rating, args=(st.session_state["word_original"]["tran_id"], 0.0,))
                st.write(f"Úspěšnost: {score if score is not None and score >= 0 else "Neznámá"}")
                if score is not None:
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=score,
                        number={"valueformat": ".2f"},
                        gauge={
                            "axis": {"range": [0, 1]},
                            "bar": {"thickness": 0.25},
                            "steps": [
                                {"range": [0, 0.33], "color": "rgba(255,0,0,0.25)"},
                                {"range": [0.33, 0.66], "color": "rgba(255,165,0,0.25)"},
                                {"range": [0.66, 1.0], "color": "rgba(0,128,0,0.25)"},
                            ],
                            "threshold": {"line": {"color": "black", "width": 3}, "value": score},
                        }
                    ))
                    fig.update_layout(
                        width=300,
                        height=250,
                        margin=dict(l=20, r=20, t=40, b=20),
                    )
                    st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Chyba při připojení na server")
if __name__ == "__main__":
    main()
