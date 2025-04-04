"""
The entry point of FastAPI application.
This file defines API routes and orchestrates
the different components of the system
"""

from model.pydantic_models import QueryInput, QueryResponse, DocumentInfo, DeleteFileRequest

from fastapi import FastAPI, File, UploadFile, HTTPException
import os
import uuid
import logging
import shutil
from typing import List

logging.basicConfig(filename='app.log', level=logging.INFO)


class App:
    def __init__(self) -> None:
        self.app: FastAPI = FastAPI()

        @self.app.post('/chat', response_model=QueryResponse)
        def chat(query_input: QueryInput) -> QueryResponse:
            pass

        @self.app.post('/upload-doc')
        def upload_and_index_document(file: UploadFile = File(...)):
            pass

        @self.app.get('/list-docs', response_model=List[DocumentInfo])
        def list_documents() -> List[DocumentInfo]:
            pass

        @self.app.post('/delete-doc')
        def delete_document(request: DeleteFileRequest):
            pass

    def run(self) -> None:
        pass
