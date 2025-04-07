"""
This file is the entry point for Streamlit application.
"""


from ui.components.sidebar import Sidebar
from ui.components.chat_interface import ChatInterface

import streamlit as st


class StreamlitApp:
    def __init__(self) -> None:
        self.sidebar: Sidebar = Sidebar()
        self.chat_interface: ChatInterface = ChatInterface()

    def run(self) -> None:
        """
        Initiates launch of the application
        :return:
        """

        st.title('Langchain RAG Chatbot')

        # Initialize session state variables
        if 'messages' not in st.session_state:
            st.session_state.messages = []

        if 'session_id' not in st.session_state:
            st.session_state.session_id = None

        # Displaying components
        self.sidebar.display()
        self.chat_interface.display()
