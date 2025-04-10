"""
This file defines Pydantic models for request
and response validation, ensuring
type safety and clear API contracts
"""

from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime


class ModelName(str, Enum):
    """
    Defines the available language models for system
    """

    # OpenAI models
    GPT4_O = 'gpt-4o'
    GPT4_0_MINI = 'gpt-4o-mini'
    GPT3_5_TURBO = 'gpt-3.5-turbo'

    # Llama models
    LLAMA3 = 'llama3'
    LLAMA2 = 'llama2'


class QueryInput(BaseModel):
    """
    Represents the input for a char query
    """

    question: str
    session_id: str = Field(default=None)
    model: ModelName = Field(default=ModelName.GPT4_0_MINI)


class QueryResponse(BaseModel):
    """
    Represents the response for a char query
    """

    answer: str
    session_id: str
    model: ModelName


class DocumentInfo(BaseModel):
    """
    Represents metadata about an indexed document
    """

    id: int
    filename: str
    upload_timestamp: datetime


class DeleteFileRequest(BaseModel):
    """
    Represents a request to delete a document
    """

    file_id: int
