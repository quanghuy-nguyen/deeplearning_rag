import os
from dotenv import load_dotenv
from rag_app.get_chroma_db import get_chroma_db

from langchain_xai import ChatXAI
from langchain_core.messages import AIMessage, HumanMessage
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import List
from dataclasses import dataclass

load_dotenv()


HISTORY_SYSTEM_PROMPT = """
Given chat history and latest user question, reformulate a question which can be understand without chat history.
Do not answer the question. Just reformulate it to a new question.
"""

HISTORY_PROMPT = ChatPromptTemplate.from_messages([
    ("system", HISTORY_SYSTEM_PROMPT),
    (MessagesPlaceholder("chat_history")),
    ("human", "{input}")
])

QA_SYSTEM_PROMPT = """
You are a helpful assistant. Answer the question based on follwing context:
{context}
"""

QA_PROMPT = ChatPromptTemplate.from_messages([
    ("system", QA_SYSTEM_PROMPT),
    ("human", "{input}")
])


@dataclass
class QuerryResponse:
    query_text: str
    response_text: str
    sources: List[str]
    chat_history: List


def query_rag(chat_history: List, query_text: str) -> QuerryResponse:
    db = get_chroma_db()
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k":3})
    llm = ChatXAI(model="grok-2-1212")

    history_retriever = create_history_aware_retriever(llm, retriever, HISTORY_PROMPT)
    answer = create_stuff_documents_chain(llm=llm, prompt=QA_PROMPT)
    rag_chain = create_retrieval_chain(history_retriever, answer)

    results = rag_chain.invoke({"input": query_text, "chat_history": chat_history})
    sources = [doc.metadata["source"] for doc in results["context"]]

    chat_history.append(HumanMessage(content=query_text))
    chat_history.append(AIMessage(content=results["answer"]))

    return QuerryResponse(
        query_text=query_text,
        response_text=results["answer"],
        sources=sources,
        chat_history=chat_history
    )


def main():
    chat_history = []
    while True:
        message = input("You: ")
        if message == "exit":
            break
        result = query_rag(chat_history, message)
        print("-"*50)
        print("Source")
        print(result.sources)
        print("-"*50)

        print("-"*50)
        print("Answer")
        print(result.response_text)
        print("-"*50)

        print("-"*50)
        print("Chat history")
        print(result.chat_history)
        print("-"*50)




# if __name__ == "__main__":
#     main()