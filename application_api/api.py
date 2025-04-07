"""
The entry point of FastAPI application.
This file defines API routes and orchestrates
the different components of the system
"""

from application_api.model.pydantic_models import QueryInput, QueryResponse, DocumentInfo, DeleteFileRequest
from application_api.utils.chroma_utils import ChromaUtils
from application_api.utils.langchain_utils import LangChainUtils
from application_api.utils.db_utils import DBUtils

from fastapi import FastAPI, File, UploadFile, HTTPException
import os
import uuid
import logging
import shutil
from typing import List, Dict, Text, Any

logging.basicConfig(filename='app.log', level=logging.INFO)


class App:
    def __init__(self) -> None:
        self.app: FastAPI = FastAPI()

        self.db_utils: DBUtils = DBUtils()
        self.langchain_utils: LangChainUtils = LangChainUtils()
        self.chroma_utils: ChromaUtils = ChromaUtils()

        @self.app.post('/chat', response_model=QueryResponse)
        def chat(query_input: QueryInput) -> QueryResponse:
            """
            Endpoint, that handles chat operations
            :param query_input:
            :return:
            """

            session_id: str = query_input.session_id or str(uuid.uuid4())
            logging.info(
                f'Session ID: {session_id}, User Query: {query_input.question}, Model: {query_input.model.value}'
            )

            chat_history: List[Dict[Text, Text]] = self.db_utils.get_chat_history(session_id)
            rag_chain: Any = self.langchain_utils.get_rag_chain()

            answer = rag_chain.invoke({
                'input': query_input.question,
                'chat_history': chat_history
            })['answer']
            self.db_utils.insert_application_logs(session_id, query_input.question, answer, query_input.model.value)
            logging.info(f'Session ID: {session_id}, AI Response: {answer}')
            return QueryResponse(answer=answer, session_id=session_id, model=query_input.model)

        @self.app.post('/upload-doc')
        def upload_and_index_document(file: UploadFile = File(...)) -> Dict[Text, Text]:
            """
            Endpoint, that handles document upload and
            updates document record in database
            :param file:
            :return:
            """

            allowed_extensions: list[str] = ['.pdf', '.docx', '.html']
            file_extension: str = os.path.splitext(file.filename)[1].lower()

            if file_extension not in allowed_extensions:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file type. Allowed types are: {','.join(allowed_extensions)}"
                )

            temp_file_path: str = f'temp_{file.filename}'

            try:
                # Saving the uploaded file to a temporary file
                with open(temp_file_path, 'wb') as buffer:
                    shutil.copyfileobj(file.file, buffer)

                file_id: int = self.db_utils.insert_document_record(file.filename)
                success: bool = self.chroma_utils.index_document_to_chroma(temp_file_path, file_id)

                if success:
                    return {
                        'message': f'File {file.filename} has been successfully uploaded and indexed.',
                        'file_id': file_id
                    }
                else:
                    self.db_utils.delete_document_record(file_id)
                    raise HTTPException(status_code=500, detail=f'Failed to index {file.filename}')
            finally:
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)

        @self.app.get('/list-docs', response_model=List[DocumentInfo])
        def list_documents() -> List[DocumentInfo]:
            """
            Returns list of indexed documents
            :return:
            """

            documents: List[Dict] = self.db_utils.get_all_documents()
            return [
                DocumentInfo(id=doc['id'], filename=doc['filename'], upload_timestamp=doc['upload_timestamp'])
                for doc in documents
            ]

        @self.app.post('/delete-doc')
        def delete_document(request: DeleteFileRequest) -> Dict[Text, Text]:
            """
            Endpoint handles document deletion, removing
            the document from the Chroma and database
            :param request:
            :return:
            """

            chroma_delete_success: bool = self.chroma_utils.delete_doc_from_chroma(request.file_id)

            if chroma_delete_success:
                db_delete_success: bool = self.db_utils.delete_document_record(request.file_id)
                if db_delete_success:
                    return {'message': f'Successfully deleted document with file_id {request.file_id} from system.'}
                else:
                    return {'error': f'Deleted from Chroma but failed to delete document with file_id {request.file_id}'
                                     f' from the database.'}
            else:
                return {'error': f'Failed to delete document with file_id {request.file_id} from Chroma.'}

    def run(self) -> None:
        pass
