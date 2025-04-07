"""This file defines prompts for LLM"""


from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)

contextualize_q_prompt = ChatPromptTemplate.from_messages([
    ('system', contextualize_q_system_prompt),
    MessagesPlaceholder('chat_history'),
    ('human', '{input}')
])

qa_prompt = ChatPromptTemplate.from_messages([
    ('system', "You are a helpful AI assistant. Use the following context to answer the user's question."),
    ('system', 'Context: {context}'),
    MessagesPlaceholder(variable_name='chat_history'),
    ('human', '{input}')
])
