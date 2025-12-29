"""
Main program for Vodous
"""

import os
import streamlit as st
from dotenv import load_dotenv
from pages.switch_panel import main_menu
import pages.page_controller as pgs

load_dotenv()

# ENV properties
APP_BASE_URL = os.getenv("APP_BASE_URL")
APP_NAME = os.getenv("APP_NAME")

# pages
pg = pgs.PageController()
page_board         = pg.page_create("pages/board.py", "Board", "board")
page_companie      = pg.page_create("pages/flashcard.py", "Flash card", "flashcard")
page_company       = pg.page_create("pages/matching.py", "Matching", "matching")

pg.create_page_navigator()

st.set_page_config(page_title="Vodouš", page_icon="pictures/vodous_tmavy_head.png")

# main menu
main_menu()

with st.container(border=True):
    st.markdown("# VODOUŠ")

pg.run()
