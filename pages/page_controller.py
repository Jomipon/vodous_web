import streamlit as st

class PageController():
    """
    Controler for pages
    """
    def __init__(self):
        self._pages = []
        self._navigation = None

    def page_create(self, file_script, title, url_path):
        """
        Create new page for registration
        
        :param file_script: File name
        :param title: Title for menu
        :param url_path: URL path
        """
        page = st.Page(file_script,  title=title,  url_path=url_path)
        self._pages.append(page)
        return page

    def create_page_navigator(self):
        """
        Add page to navigation
        """
        self._navigation = st.navigation(self._pages, position="hidden")
    
    def run(self):
        """
        Start navigation for build
        """
        self._navigation.run()