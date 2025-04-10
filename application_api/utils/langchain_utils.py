"""
This file encapsulates the LangChain specific logic,
such as creating the RAG chain and
configuring the language model
"""

from application_api.utils.chroma_utils import ChromaUtils
from application_api.utils.langchain_prompts import contextualize_q_prompt, qa_prompt

from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from typing import Any


class LangChainUtils:
    """
    Implementation of core component of RAG system using LangChain
    """

    def __init__(self, vector_store: Chroma = ChromaUtils().vector_store) -> None:
        self.retriever = vector_store.as_retriever(search_kwargs={'k': 2})
        self.output_parser = StrOutputParser()

    def get_rag_chain(self, model='llama3') -> Any:
        """
        Creates RAG chain using LLM, history-aware retriever and question-answering chain
        :param model:
        :return:
        """

        llm: OllamaLLM = OllamaLLM(model=model)
        history_aware_retriever = create_history_aware_retriever(llm, self.retriever, contextualize_q_prompt)
        question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
        return rag_chain
