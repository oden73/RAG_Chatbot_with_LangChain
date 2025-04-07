"""
This file contains utilities for interacting
with the Chroma vector store, including
functions for indexing documents and
performing similarity searches
"""

from application_api.exceptions.file_type_exception import FileTypeException

from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredCHMLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from typing import List, Dict, Text, Any


class ChromaUtils:
    """
    Class for interaction with Chroma vector storage
    """

    CHROMA_DIRECTORY: str = r'../chroma_db'

    def __init__(self) -> None:
        self.text_splitter: RecursiveCharacterTextSplitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        self.embedding_function: OpenAIEmbeddings = OpenAIEmbeddings()
        self.vector_store: Chroma = Chroma(
            persist_directory=ChromaUtils.CHROMA_DIRECTORY,
            embedding_function=self.embedding_function
        )

    def load_and_split_document(self, file_path: str) -> List[Document]:
        """
        Analyzes file format and loads file, then splits it into chunks
        :param file_path:
        :return:
        """

        if file_path.endswith('.pdf'):
            loader: PyPDFLoader = PyPDFLoader(file_path)
        elif file_path.endswith('.docx'):
            loader: Docx2txtLoader = Docx2txtLoader(file_path)
        elif file_path.endswith('.html'):
            loader: UnstructuredCHMLoader = UnstructuredCHMLoader(file_path)
        else:
            raise FileTypeException('')

        documents: List[Document] = loader.load()
        return self.text_splitter.split_documents(documents)

    def index_document_to_chroma(self, file_path: str, file_id: int) -> bool:
        """
        Loads and splits document, then adds metadata(file_id),
        that allows to link vector store entries back to database records
        :param file_path:
        :param file_id:
        :return:
        """

        try:
            splits: List[Document] = self.load_and_split_document(file_path)

            # Adding metadata to each split
            for split in splits:
                split.metadata['file_id'] = file_id

            self.vector_store.add_documents(splits)
            return True
        except Exception as e:
            print(f'Error indexing document: {e}')
            return False

    def delete_doc_from_chroma(self, file_id: int) -> bool:
        """
        Deletes all document chunks associated with a
        given file_id from the Chroma vector store
        :param file_id:
        :return:
        """

        try:
            documents: Dict[Text, Any] = self.vector_store.get(where={'file_id': file_id})
            print(f'Found {len(documents["ids"])} document chunks for file_id {file_id}')

            self.vector_store.delete(where={'file_id': file_id})
            print(f'Deleted all documents with file_id {file_id}')

            return True
        except Exception as e:
            print(f'Error deleting document with file_id {file_id} from Chroma: {str(e)}')
            return False
