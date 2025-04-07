"""
This file contains API interaction utils
"""

import requests
import streamlit as st
from typing import Dict, Text, Any


class APIUtils:
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_api_response(question: str, session_id: str, model: str) -> Any:
        """
        Sends chat queries and receives responses.
        :param question:
        :param session_id:
        :param model:
        :return:
        """

        headers: Dict[Text, Text] = {'accept': 'application/json', 'Content-Type': 'application/json'}
        data: Dict[Text, Text] = {'question': question, 'model': model}
        if session_id:
            data['session_id'] = session_id

        try:
            response: requests.Response = requests.post(
                url='http://localhost:8000/chat', headers=headers, json=data
            )
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f'API request failed with status code {response.status_code}: {response.text}')
                return None
        except Exception as e:
            st.error(f'An error occurred: {str(e)}')
            return None

    @staticmethod
    def upload_document(file) -> Any:
        """
        Handles file uploads to the backend.
        :param file:
        :return:
        """

        try:
            files: Dict[Text, Any] = {'file': (file.name, file, file.type)}
            response: requests.Response = requests.post(
                url='http://localhost:8000/upload-doc', files=files
            )
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f'Failed to upload file. Error: {response.status_code} - {response.text}')
                return None
        except Exception as e:
            st.error(f'An error occurred while uploading the file: {str(e)}')
            return None

    @staticmethod
    def list_documents() -> Any:
        """
        Retrieves the list of uploaded documents.
        :return:
        """

        try:
            response: requests.Response = requests.get(url='http://localhost:8000/list-docs')
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f'Failed to fetch document list. Error: {response.status_code} - {response.text}')
                return []
        except Exception as e:
            st.error(f'An error occurred while fetching the document list: {str(e)}')
            return []

    @staticmethod
    def delete_document(file_id: int) -> Any:
        """
        Sends requests to delete specific documents.
        :param file_id:
        :return:
        """

        headers: Dict[Text, Text] = {'accept': 'application/json', 'Content-Type': 'application/json'}
        data: Dict[Text, int] = {'file_id': file_id}

        try:
            response: requests.Response = requests.post(
                url='http://localhost:8000/delete-doc', headers=headers, json=data
            )
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f'Failed to delete document. Error: {response.status_code} - {response.text}')
                return None
        except Exception as e:
            st.error(f'An error occurred while deleting the document: {str(e)}')
            return None
