import os
import json
from uuid import uuid4
import streamlit as st
from dotenv import load_dotenv
from support import download_get_url, download_post_url


def main():
    """
    Main method for matching
    """
    load_dotenv()

    relationship_types = {
        0: "Random",
        1: "Custom"
    }
    st.session_state.setdefault("topic", "")
    st.session_state["topic_ready"] = len(st.session_state["topic"]) > 0
    st.session_state.setdefault("story_ready", False)
    st.session_state.setdefault("student_version", "")
    st.session_state.setdefault("student_version_ready", False)
    st.session_state.setdefault("result_ready", False)
    st.session_state.setdefault("story_level", "")
    st.session_state.setdefault("story_title", "")
    st.session_state.setdefault("story_text", "")
    st.session_state.setdefault("story_word_count", "")
    st.session_state.setdefault("story_vocab", "")
    st.session_state.setdefault("story_questions", "")


    st.markdown("<h2><b>Story Telling</b></h2>",unsafe_allow_html=True)
    with st.container(border=True):
        st.radio("Téma:",
                    options=list(relationship_types.keys()),
                    horizontal=True,
                    format_func=lambda k: relationship_types[k],
                    key="topic_radio")
        col_gen, col_man = st.columns((8,40))
        with col_gen:
            if st.button("Random topic", disabled=st.session_state['topic_radio'] == 1):
                url_base = os.getenv("FAST_API_URL_BASE")
                url_topic = os.getenv("FAST_API_URL_STORYTELLING_TOPIC")
                url = url_base + url_topic
                topic_data = download_get_url(url)
                if topic_data["status"] == 200:
                    topic = json.loads(topic_data["data"])["data"]["topic_text"]
                else:
                    topic = ""
                st.session_state["topic"] = topic
                st.session_state["topic_ready"] = len(st.session_state["topic"]) > 0
        with col_man:
            st.text_input("Topic", key="topic", disabled=st.session_state['topic_radio'] == 0) #, value=st.session_state.get('topic')

    st.markdown('<h3><b>Topic:</b></h3>',unsafe_allow_html=True)
    st.markdown(f'<b>{st.session_state.get('topic', '')}</b>',unsafe_allow_html=True)

    if st.button("Generate story", disabled=not st.session_state["topic_ready"]):
        url_base = os.getenv("FAST_API_URL_BASE")
        url_story = os.getenv("FAST_API_URL_STORYTELLING_STORY")
        url = url_base + url_story
        story_data = download_post_url(url, json.dumps({"topic": st.session_state["topic"]}),["Content-Type: application/json"])
        story_data = json.loads(story_data.decode("utf-8"))
        if story_data["status"] == "OK":
            story_data = story_data["data"]
            st.session_state["story_level"] = story_data["level"]
            st.session_state["story_title"] = story_data["title"]
            st.session_state["story_text"] = story_data["text"]
            st.session_state["story_word_count"] = story_data["word_count"]
            st.session_state["story_vocab"] = story_data["vocab"]
            st.session_state["story_questions"] = story_data["questions"]
            st.session_state["story_ready"] = True
        else:
            st.error("Error in communation with server")
    if st.session_state["story_ready"]:
        st.markdown(f'<h2><b>{st.session_state["story_title"]}</b></h2>',unsafe_allow_html=True)
        st.markdown(f'<i>{st.session_state["story_level"]} ({st.session_state["story_word_count"]} words)</i>',unsafe_allow_html=True)
        st.markdown(f'{st.session_state["story_text"]}',unsafe_allow_html=True)
        st.markdown(f'{st.session_state["story_vocab"]}',unsafe_allow_html=True)
        st.markdown(f'<b><i>{st.session_state["story_questions"]}</i></b>',unsafe_allow_html=True)
        
        st.text_area("Your version:", key="student_version")
    
    st.session_state["student_version_ready"] = len(st.session_state["student_version"]) > 0
    if st.button("Send", disabled=not st.session_state["student_version_ready"]):
        url_base = os.getenv("FAST_API_URL_BASE")
        url_evaluation = os.getenv("FAST_API_URL_STORYTELLING_EVALUATION")
        url = url_base + url_evaluation
        evaluation_data = download_post_url(url, json.dumps({"original": st.session_state["story_text"], "student": st.session_state["student_version"]}),["Content-Type: application/json"])
        evaluation_data = json.loads(evaluation_data.decode("utf-8"))
        st.session_state["result_corrected_text"] = evaluation_data["corrected_text"]
        st.session_state["result_score"] = evaluation_data["score_0_100"]
        st.session_state["result_level"] = evaluation_data["cefr_estimate"]
        st.session_state["result_feedback"] = evaluation_data["short_feedback"]
        st.session_state["result_strengths"] = evaluation_data["strengths"]
        st.session_state["result_improvements"] = evaluation_data["improvements"]
        st.session_state["result_top_corrections"] = evaluation_data["top_corrections"]
        st.session_state["result_ready"] = True
    if st.session_state["result_ready"]:
        st.markdown("<h2><b>Result:</b></h2>",unsafe_allow_html=True)
        st.markdown("<h3><b>Corrected text:</b></h3>",unsafe_allow_html=True)
        st.write(st.session_state["result_corrected_text"])
        st.markdown(f"Score (0-100): <b>{st.session_state["result_score"]}</b>",unsafe_allow_html=True)
        st.markdown(f"Level: <b>{st.session_state["result_level"]}</b>",unsafe_allow_html=True)
        st.markdown("<h3><b>Feedback:</b></h3>",unsafe_allow_html=True)
        st.write(f"{st.session_state["result_feedback"]}")
        st.markdown("<h3><b>Strenghts:</b></h3>",unsafe_allow_html=True)
        for strenght in st.session_state["result_strengths"]:
            st.write(f"{strenght}")
        st.markdown("<h3><b>Improvements:</b></h3>",unsafe_allow_html=True)
        for improvement in st.session_state["result_improvements"]:
            st.write(f"{improvement}")
        st.markdown("<h3><b>Result top corrections:</b></h3>",unsafe_allow_html=True)
        for correction in st.session_state["result_top_corrections"]:
            st.write(f"{correction}")


if __name__ == "__main__":
    main()


