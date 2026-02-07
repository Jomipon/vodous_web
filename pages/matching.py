"""
Second game
Connect same words in other language
"""
import os
import json
from uuid import uuid4
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


def find_new_word(word_alias_name):
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
    st.session_state[word_alias_name] = new_word

class WordButtonState():
    """
    word with state in page
    """
    word_id_from: str
    word_id_to: str
    word_content: str
    word_enabled: bool
    word_choosed: bool
    word_translate_id: str
    word_order_id: str

    def __init__(self, id_from: str, id_to: str, content: str, enabled: bool, choosed: bool, translate_id: str):
        """
        Inicializace
        
        :param self: Description
        :param id_from: ID from
        :type id_from: str
        :param id_to: ID to
        :type id_to: str
        :param content: Word content
        :type content: str
        :param enabled: Botton enabled
        :type enabled: bool
        :param choosed: Choesed botton
        :type choosed: bool
        :param translate_id: ID word translate
        :type translate_id: str
        """
        self.word_id_from = id_from
        self.word_id_to = id_to
        self.word_content = content
        self.word_enabled = enabled
        self.word_choosed = choosed
        self.word_translate_id = translate_id
        self.word_order_id = str(uuid4())

def button_onclick(word_id: str):
    """
    Click to choose word
    
    :param word_id: Word ID
    :type word_id: str
    """
    if "words_all" not in st.session_state:
        return 
    # get all selected word
    word_clicked = [word for word in st.session_state["words_all"] if word.word_id_from == word_id or word.word_id_to == word_id]
    if len(word_clicked) == 0:
        return 
    word_clicked = word_clicked[0]
    if word_clicked.word_choosed:
        # click -> unclick
        word_clicked.word_choosed = False
    else:
        # unclick -> click
        if word_clicked.word_id_from and word_clicked.word_id_from == word_id:
            # word from
            for word_from in [word for word in st.session_state["words_all"] if word.word_id_from]:
                word_from.word_choosed = False
        else:
            # word to
            for word_from in [word for word in st.session_state["words_all"] if word.word_id_to]:
                word_from.word_choosed = False
        word_clicked.word_choosed = True
    words_from_checked = [word for word in st.session_state["words_all"] if word.word_id_from and word.word_choosed]
    words_to_checked = [word for word in st.session_state["words_all"] if word.word_id_to and word.word_choosed]
    if len(words_from_checked) > 0 and len(words_to_checked) > 0:
        if words_from_checked[0].word_translate_id == words_to_checked[0].word_id_to and words_to_checked[0].word_translate_id == words_from_checked[0].word_id_from:
            words_from_checked[0].word_enabled = False
            words_from_checked[0].word_choosed = False
            words_to_checked[0].word_enabled = False
            words_to_checked[0].word_choosed = False
        else:
            words_from_checked[0].word_choosed = False
            words_to_checked[0].word_choosed = False
    if len([word for word in st.session_state["words_all"] if word.word_enabled]) == 0:
        st.session_state["words_all"] = []
        st.session_state.pop("words_all")

def main():
    """
    Main method for matching
    """
    load_dotenv()

    matching_word_count = os.getenv("MATCHING_WORD_COUNT", "4")
    try:
        matching_word_count = int(matching_word_count)
    except:
        matching_word_count = 4
    
    st.write("Matching")

    if "words_all" not in st.session_state:
        data = []
        for index in range(matching_word_count):
            find_new_word(f"word_{index}")
            data.append(WordButtonState(st.session_state[f"word_{index}"]["orig_word_id"], "", st.session_state[f"word_{index}"]["orig_word"], True, False, st.session_state[f"word_{index}"]["tran_word_id"]))
            data.append(WordButtonState("", st.session_state[f"word_{index}"]["tran_word_id"], st.session_state[f"word_{index}"]["tran_word"], True, False, st.session_state[f"word_{index}"]["orig_word_id"]))
        data.sort(key=lambda x: x.word_order_id)
        st.session_state["words_all"] = data
    #CSS for button primary / secondary
    st.markdown("""
    <style>
    /* secondary = turn off */
    button[data-testid="baseButton-secondary"] {
    background-color: #1f2937 !important;  /* tmavá */
    color: white !important;
    }

    /* primary = turn on */
    button[data-testid="baseButton-primary"] {
    background-color: #22c55e !important;  /* zelená */
    color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)
    col_from, col_to = st.columns([1,2])
    for word_button in st.session_state["words_all"]:
        button_type = ""
        buttone_enabled = True
        word_id = ""
        if word_button.word_id_from:
            word_id = word_button.word_id_from
        else:
            word_id = word_button.word_id_to
        if not word_button.word_enabled:
            button_type = "secondary"
            buttone_enabled = False
        elif word_button.word_choosed:
            button_type = "primary"
            buttone_enabled = True
        else:
            button_type = "secondary"
            buttone_enabled = True
        if word_button.word_id_from:
            col = col_from
        else:
            col = col_to
        with col:
            st.button(word_button.word_content,
                    type=button_type,
                    disabled=not buttone_enabled,
                    key=f"btn_{word_id}",
                    on_click=button_onclick, args=(word_id,))
if __name__ == "__main__":
    main()
