import os
import json
from typing import Annotated
from fastapi import FastAPI, HTTPException, status, Header, UploadFile
from schema import Chat, ChatResponse
from utils import (
    save_and_verify_docs,
)
from llama_deploy import LlamaDeployClient, ControlPlaneConfig
from llama_index.llms.ollama import Ollama

client = LlamaDeployClient(ControlPlaneConfig())

app = FastAPI()


@app.post("/upload_document")
async def upload_documents(
    file: UploadFile,
    mobile_id: Annotated[str | None, Header()],
):
    file_name = file.filename
    file_content_type = file.content_type
    content = await file.read()

    # Replace cloud storage with below function
    doc_id = save_and_verify_docs(
        file_content_type=file_content_type, file_name=file_name, file_content=content
    )

    return {"document_id": doc_id}


@app.post("/chat")
async def chat_llama(
    chat: Chat, mobile_id: Annotated[str | None, Header()]
) -> ChatResponse:
    session = client.get_or_create_session(session_id=mobile_id)

    query = chat.query

    if chat.document_id is not None:
        response = session.run("security_layer_agent", query=query)

        if response == "granted":
            # response, reference = session.run("docs_agent", query=query, document_id=chat.document_id)
            return ChatResponse(bot_message=query, reference=query)
        else:
            response = "I'm designed to help with order-related tasks and questions about user documents. Unfortunately, I can't assist with your current request. Feel free to ask me something else within those parameters."
    else:
        response = session.run("security_layer_agent", query=query)

        if response == "granted":
            if chat.agent_id == "order_agent":
                response = session.run("order_agent", query=query)
                # pass
            elif chat.agent_id == "knowledge_agent":
                # response = session.run("knowledge_agent", query=query)
                pass
            else:
                response = session.run("order_agent", query=query)
                # response = session.run("multi_agent", query=query)
                pass
        else:
            response = "I'm designed to help with order-related tasks and questions about user documents. Unfortunately, I can't assist with your current request. Feel free to ask me something else within those parameters."

    return ChatResponse(bot_message=response)
