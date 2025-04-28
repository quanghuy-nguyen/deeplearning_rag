from query_model import QueryModel
from rag_app.query_rag import query_rag

chat_history = []

def handler(event, context):
    query_item = QueryModel(**event)
    invoke_rag(query_item)


def invoke_rag(query_item: QueryModel):
    global chat_history

    response = query_rag(chat_history=chat_history, query_text=query_item.query_text)
    chat_history = response.chat_history

    query_item.answer_text = response.response_text
    query_item.sources = response.sources
    query_item.is_completed = True

    query_item.put_item()
    print(f"Item is updated {query_item}")