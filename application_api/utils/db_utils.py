"""
This file handles database operations,
including storing and retrieving chat history and
document metadata
"""

import sqlite3
from typing import Dict, List, Text, Tuple


class DBUtils:
    """
    Class for interactions with SQLite database
    """

    DB_NAME: str = 'rag_app.db'

    def __init__(self) -> None:
        pass

    @staticmethod
    def get_db_connection() -> sqlite3.Connection:
        """
        Creates connection to SQLite database
        :return:
        """

        connection: sqlite3.Connection = sqlite3.connect(DBUtils.DB_NAME)
        connection.row_factory = sqlite3.Row
        return connection

    def create_application_logs(self) -> None:
        """
        Stores chat history and model responses
        :return:
        """

        connection: sqlite3.Connection = self.get_db_connection()
        connection.execute('''CREATE TABLE IF NOT EXISTS application_logs
                              (id INTEGER PRIMARY KEY AUTOINCREMENT,
                               session_id TEXT,
                               user_query TEXT,
                               gpt_response TEXT,
                               model TEXT,
                               created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        connection.close()

    def create_document_store(self) -> None:
        """
        Keeps track of uploaded documents
        :return:
        """

        connection: sqlite3.Connection = self.get_db_connection()
        connection.execute('''CREATE TABLE IF NOT EXISTS document_store
                              (id INTEGER PRIMARY KEY AUTOINCREMENT,
                               filename TEXT,
                               upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        connection.close()

    def insert_application_logs(self, session_id: str, user_query: str, gpt_response: str, model: str) -> None:
        """
        Inserts log into application_logs table in database
        :param session_id:
        :param user_query:
        :param gpt_response:
        :param model:
        :return:
        """

        connection: sqlite3.Connection = self.get_db_connection()
        connection.execute(
            'INSERT INTO application_logs (session_id, user_query, gpt_response, model) VALUES (?, ?, ?, ?)',
            (session_id, user_query, gpt_response, model)
        )
        connection.commit()
        connection.close()

    def get_chat_history(self, session_id: str) -> List[Dict[Text, Text]]:
        """
        Retrieves chat history from application_logs using session_id
        :param session_id:
        :return:
        """
        connection: sqlite3.Connection = self.get_db_connection()
        cursor: sqlite3.Cursor = connection.cursor()
        messages: List[Dict[Text, Text]] = []

        cursor.execute(
            'SELECT user_query, gpt_response FROM application_logs WHERE session_id = ? ORDER BY created_at',
            (session_id,)
        )
        for row in cursor.fetchall():
            messages.extend([
                {'role': 'human', 'content': row['user_query']},
                {'role': 'ai', 'content': row['gpt_response']}
            ])

        connection.close()
        return messages

    def insert_document_record(self, filename: str) -> int:
        """
        Inserts new document record in document_store table
        :param filename:
        :return:
        """

        connection: sqlite3.Connection = self.get_db_connection()
        cursor: sqlite3.Cursor = connection.cursor()
        cursor.execute('INSERT INTO document_store (filename) VALUES (?)', (filename,))
        file_id: int = cursor.lastrowid
        connection.commit()
        connection.close()
        return file_id

    def delete_document_record(self, file_id: int) -> bool:
        """
        Deletes document record from document_store table
        :param file_id:
        :return:
        """

        connection: sqlite3.Connection = self.get_db_connection()
        connection.execute('DELETE FROM document_store WHERE id = ?', (file_id,))
        connection.commit()
        connection.close()
        return True

    def get_all_documents(self) -> List[Dict[Text, Text]]:
        """
        Retrieves all document records from document_store table
        :return:
        """

        connection: sqlite3.Connection = self.get_db_connection()
        cursor: sqlite3.Cursor = connection.cursor()
        cursor.execute('SELECT id, filename, upload_timestamp FROM document_store ORDER BY upload_timestamp DESC')
        documents: List[Tuple] = cursor.fetchall()
        connection.close()
        return [dict(doc) for doc in documents]
