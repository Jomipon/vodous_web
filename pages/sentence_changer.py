import os
import json
from uuid import uuid4
import streamlit as st
from dotenv import load_dotenv
from support import download_get_url, download_post_url


def download_tenses():
    url_base = os.getenv("FAST_API_URL_BASE")
    url_sentence_tenses = os.getenv("FAST_API_URL_SENTENCE_ALL_TENSES")
    url = url_base + url_sentence_tenses
    sentence_tenses = download_get_url(url)
    return sentence_tenses
def load_tenses():
    if "tenses" not in st.session_state:
        tenses = download_tenses()
        if tenses["status"] == 200:
            tenses_name = []
            for tense in json.loads(tenses["data"])["data"]:
                tenses_name.append(tense["text_eng"])
            st.session_state["tenses"] = tenses_name
            #st.write(json.loads(tenses["data"])["data"][0]["text_eng"])
    
def main():
    """
    Main method for sentence changing
    """
    load_dotenv()

    load_tenses()

    st.markdown("<h2><b>Sentence changing</b></h2>",unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<h3><b>Input configuration</b></h3>",unsafe_allow_html=True)
        st.radio("Tense of sentence:",
                    options=list(st.session_state["tenses"]),
                    horizontal=True,
                    key="sentence_source_tense")
        st.radio("Type of sentence:",
                    options=list(["positive","negative","question"]),
                    horizontal=True,
                    key="sentence_source_tense_type")
        if st.button("Generate"):
            url_base = os.getenv("FAST_API_URL_BASE")
            url_sentence_random = os.getenv("FAST_API_URL_SENTENCE_RANDOM")
            url = url_base + url_sentence_random
            post_data = {"Tense": st.session_state.get("sentence_source_tense","Present simple"), "Type": st.session_state.get("sentence_source_tense_type","positive")}
            sentence_random = download_post_url(url, post_data=json.dumps(post_data), headers=["Content-Type: application/json"])
            sentence_random = json.loads(sentence_random)
            #st.write(f"{sentence_random["data"]["text_eng"]=}")
            #st.write(f"{sentence_random["data"]["text_cz"]=}")
            #st.write(f"{sentence_random["data"]["tense_id"]=}")
            #st.write(f"{sentence_random["data"]["sentence_type"]=}")
            st.session_state["sentence_source_eng"] = sentence_random["data"]["text_eng"]
            st.session_state["sentence_source_cz"] = sentence_random["data"]["text_cz"]
            st.session_state["sentence_target_tense"] = st.session_state["sentence_source_tense"]
            st.session_state["sentence_target_tense_type"] = st.session_state["sentence_source_tense_type"]
            st.session_state["sentence_target_eng"] = ""
        #st.write("Sentence")
        #st.text_input("Sentence:", key="sentence_source_eng", disabled=True)
        st.write(f"Sentence ENG: {st.session_state.get('sentence_source_eng', '')}")
        st.write(f"Sentence CZ: {st.session_state.get('sentence_source_cz', '')}")
        
    with st.container(border=True):
        st.text_input("New sentence:", key="sentence_target_eng")
        st.radio("Tense of sentence:",
                    options=list(st.session_state["tenses"]),
                    horizontal=True,
                    key="sentence_target_tense")
        st.radio("Type of sentence:",
                    options=list(["positive","negative","question"]),
                    horizontal=True,
                    key="sentence_target_tense_type")
        if st.button("Check"):
            url_base = os.getenv("FAST_API_URL_BASE")
            url_sentence_check = os.getenv("FAST_API_URL_SENTENCE_CHECK")
            url = url_base + url_sentence_check
            post_data = {
                "SourceSentence": st.session_state.get("sentence_source_eng",""),
                "NewSentence": st.session_state.get("sentence_target_eng",""),
                "TargetTense": st.session_state.get("sentence_target_tense",""), 
                "TargetTenseType": st.session_state.get("sentence_target_tense_type","")
                }
            sentence_check = download_post_url(url, post_data=json.dumps(post_data), headers=["Content-Type: application/json"])
            sentence_check = json.loads(sentence_check)["data"]
            st.session_state["sentence_check"] = sentence_check

    with st.container(border=True):
        if "sentence_check" in st.session_state:
            st.write(f"{st.session_state['sentence_check']['tense']} - {st.session_state['sentence_check']['target_sentence_type']}")
            if st.session_state['sentence_check']['is_correct']:
                st.write("Check: :+1:")
            else:
                st.write("Check: :x:")
            if st.session_state['sentence_check']['kept_meaning']:
                st.write("Keep meaning: :+1:")
            else:
                st.write("Keep meaning: :x:")
            if st.session_state['sentence_check']['kept_phrasal_verb']:
                st.write("Keep phrasal verb: :+1:")
            else:
                st.write("Keep phrasal verb: :x:")
            #st.write(f"{st.session_state['sentence_check']['is_correct']=}")
            #st.write(":white_check_mark:  :negative_squared_cross_mark:")
            #st.write(":heavy_check_mark:  :heavy_multiplication_x:")
            #st.write(":ballot_box_with_check:")
            #st.write(":+1:   :-1:")
            #st.write(":x:")
            st.write(f"Edited: {st.session_state['sentence_target_eng']}")
            st.write(f"Correct: {st.session_state['sentence_check']['corrected_sentence']}")
            st.write(f"CZ: {st.session_state['sentence_check']['corrected_czech_translation']}")
            #st.write(f"{st.session_state['sentence_check']['errors']=}")
            if len(st.session_state['sentence_check']['errors']) > 0:
                st.write("Errors")
                for error in st.session_state['sentence_check']['errors']:
                    st.write(f"{error['category']=}")
                    st.write(f"{error['problem']=}")
                    st.write(f"{error['fix']=}")
            st.write(f"Feedback CZ {st.session_state['sentence_check']['short_feedback_cz']}")
            st.write("Tips CZ")
            for feedback in st.session_state['sentence_check']['tips_cz']:
                st.write(f"{feedback}")


if __name__ == "__main__":
    main()


 
