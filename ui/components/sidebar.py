"""
File contains Streamlit application sidebar.
Sidebar handles document managing and model selection.
"""

from ui.utils.api_utils import APIUtils

import streamlit as st
from typing import List, Text, Any


class Sidebar:
    def __init__(self) -> None:
        self.api_utils: APIUtils = APIUtils()

    def display(self) -> None:
        """
        Functionality to handle user document managing and model selection.
        :return:
        """

        # Model selection
        model_options: List[Text] = ['gpt-4o', 'gpt-4o-mini']
        st.sidebar.selectbox('Select Model', options=model_options, key='model')

        # Document upload
        uploaded_file = st.sidebar.file_uploader('Choose a file', type=['pdf', 'docx', 'html'])
        if uploaded_file and st.sidebar.button('Upload'):
            with st.spinner('Uploading...'):
                upload_response: Any = self.api_utils.upload_document(uploaded_file)
                if upload_response:
                    st.sidebar.success(f"File uploaded successfully with ID {upload_response['file_id']}.")
                    st.session_state.documents = self.api_utils.list_documents()

        # List and delete documents
        st.sidebar.header('Uploaded Documents')
        if st.sidebar.button('Refresh Document List'):
            st.session_state.documents = self.api_utils.list_documents()

        # Display document list and delete functionality
        if 'documents' in st.session_state and st.session_state.documents:
            for doc in st.session_state.documents:
                st.sidebar.text(f"{doc['filename']} (ID {doc['id']})")

            selected_file = st.sidebar.selectbox(
                'Select document to delete',
                options=[doc['id'] for doc in st.session_state.documents]
            )
            if st.sidebar.button('Delete Selected Document'):
                delete_response: Any = self.api_utils.delete_document(selected_file)
                if delete_response:
                    st.sidebar.success(f"Successfully deleted document with ID {selected_file}")
                    st.session_state.documents = self.api_utils.list_documents()
