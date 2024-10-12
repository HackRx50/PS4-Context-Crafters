import os
import json
from typing import Annotated
from fastapi import FastAPI, HTTPException, status, Header, UploadFile
from schema import Chat, ChatResponse, DocLoad
from utils import (
    save_and_verify_docs,
)

# from llama_deploy import LlamaDeployClient, ControlPlaneConfig
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
import uuid


# client = LlamaDeployClient(ControlPlaneConfig())

app = FastAPI()

account_url = "https://hackerxdocs.blob.core.windows.net"
default_credential = DefaultAzureCredential(
    # exclude_interactive_browser_credential=False,
    additionally_allowed_tenants=["a5f0da40-e55f-483b-a42e-a802ecc4db61"],
)


@app.post("/upload_document")
async def upload_documents(
    file: UploadFile,
    mobile_id: Annotated[str | None, Header()],
):
    file_name = file.filename
    file_content_type = file.content_type
    content = await file.read()
    if file_content_type == "pdf":
        ext = ".pdf"
    elif file_content_type == "json":
        ext = ".json"
    elif file_content_type == "docx":
        ext = ".docx"
    else:
        ext = ".txt"
    blob_service_client = BlobServiceClient(account_url, credential=default_credential)

    container_list = blob_service_client.list_containers()
    if mobile_id not in container_list:
        container_client = blob_service_client.create_container(mobile_id)

    blob_id = str(uuid.uuid4()) + ext
    blob_client = blob_service_client.get_blob_client(container=mobile_id, blob=blob_id)

    blob_client.upload_blob(content)
    # Replace cloud storage with below function
    # doc_id = save_and_verify_docs(
    #     file_content_type=file_content_type, file_name=file_name, file_content=content
    # )
    doc_id = blob_id

    return {"document_id": doc_id}


@app.get("/load_document")
async def load(
    doc_id: DocLoad,
    mobile_id: Annotated[str | None, Header()],
):
    blob_service_client = BlobServiceClient(account_url, credential=default_credential)
    container_client = blob_service_client.get_container_client(mobile_id)
    file = await container_client.download_blob(doc_id.doc_id)
    return {"doc_content": file}


# @app.post("/chat")
# async def chat_llama(
#     chat: Chat,
#     mobile_id: Annotated[str | None, Header()]
# ) -> ChatResponse:

#     session = client.get_or_create_session(session_id=mobile_id)

#     query = chat.query
#     response = session.run("security_layer_agent", query=query)

#     if chat.document_id is not None:
#         # response, reference = session.run("docs_agent", query=query, document_id=chat.document_id)
#         return ChatResponse(bot_message=query, reference=query)

#     if chat.agent_id == "appointment_agent":
#         # response = session.run("appointment_agent", query=query)
#         pass
#     elif chat.agent_id == "knowledge_agent":
#         # response = session.run("knowledge_agent", query=query)
#         pass
#     else:
#         # response = session.run("multi_agent", query=query)
#         pass

#     return ChatResponse(bot_message=response)
