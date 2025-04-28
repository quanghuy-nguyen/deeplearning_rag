import os
import uvicorn
import boto3
import json
from fastapi import FastAPI
from mangum import Mangum
from pydantic import BaseModel
from rag_app.query_rag import query_rag
from query_model import QueryModel

WORKER_LAMBDA_NAME = os.environ.get("WORKER_LAMBDA_NAME", None)


app = FastAPI()
handler = Mangum(app)
chat_history = []


class SubmitQueryRequest(BaseModel):
    query_text: str



@app.get("/")
def index():
    return {"HELLO": "I am an RAG chatbot"}


@app.get("/get_query")
def get_query_endpoint(query_id: str) -> QueryModel:
    query = QueryModel.get_item(query_id=query_id)
    return query


@app.post("/submit_query")
def submit_query_endpoint(request: SubmitQueryRequest) -> QueryModel:
    global chat_history
    new_query = QueryModel(query_text=request.query_text)

    if WORKER_LAMBDA_NAME:
        new_query.put_item()
        invoke_worker(new_query)

    else:
        response = query_rag(chat_history=chat_history, query_text=request.query_text)
        chat_history = response.chat_history

        new_query.answer_text = response.response_text
        new_query.sources = response.sources
        new_query.is_completed = True

        new_query.put_item()

    return new_query


def invoke_worker(new_query: QueryModel):
    lambda_client = boto3.client("lambda")

    payload = new_query.model_dump() # covert to dict

    response = lambda_client.invoke(
        FunctionName=WORKER_LAMBDA_NAME,
        InvocationType="Event",
        Payload=json.dumps(payload)
    )

    print(f"Worker lambda invoke {response}")



if __name__ == "__main__":
    port = 8000
    print(f"Running FastAPI server on port {port}")
    uvicorn.run("app_api_handler:app", host="0.0.0.0", port=port)


