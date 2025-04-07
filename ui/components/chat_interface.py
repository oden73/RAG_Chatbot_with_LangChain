"""
This file implements user interaction with chat.
"""

from ui.utils.api_utils import APIUtils

import streamlit as st
from typing import Any


class ChatInterface:
    def __init__(self) -> None:
        self.api_utils: APIUtils = APIUtils()

    def display(self) -> None:
        """
        Handles main chat interactions
        :return:
        """

        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message['role']):
                st.markdown(message['content'])

        # Handle new user input
        if prompt := st.chat_input('Query:'):
            st.session_state.messages.append({'role': 'user', 'content': prompt})
            with st.chat_message('user'):
                st.markdown(prompt)

            # Get AI response
            with st.spinner('Generating response...'):
                response: Any = self.api_utils.get_api_response(
                    question=prompt, session_id=st.session_state.session_id, model=st.session_state.model
                )

                if response:
                    st.session_state.session_id = response.get('session_id')
                    st.session_state.messages.append({'role': 'ai', 'content': response['answer']})

                    with st.chat_message('ai'):
                        st.markdown(response['answer'])

                    with st.expander('Details'):
                        st.subheader('Generated Answer')
                        st.code(response['answer'])
                        st.subheader('Model Used')
                        st.code(response['model'])
                        st.subheader('Session ID')
                        st.code(response['session_id'])
                else:
                    st.error('Failed to get response from the API. Please try again.')
