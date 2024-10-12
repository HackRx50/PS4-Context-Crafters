import os
import json
from typing import Annotated
from fastapi import FastAPI, HTTPException, status, Header, UploadFile
from schema import Token, Session, ViewUser, Chat, ChatResponse
from utils import (
    authenticate_user,
    load_database,
    create_user,
    generate_unique_id,
    verify_user,
    save_and_verify_docs,
)

from llama_deploy import LlamaDeployClient, ControlPlaneConfig

client = LlamaDeployClient(ControlPlaneConfig())

user_db = load_database("user")
doc_db = load_database("documents")

app = FastAPI()


@app.post("/login")
async def login_for_session_id(user: ViewUser) -> Session:
    user_id = authenticate_user(user_db, user)
    session_id = "9YhNJWP"  # generate_unique_id()
    user_db["sessions"][session_id] = user_id

    return Session(user_id=user_id, session_id=session_id)


@app.post("/signup")
async def signup_for_new_user(user: ViewUser) -> Token:
    create_user(user_db, user)
    return Token(user_id=user.user_id)


@app.post("/upload_document")
async def upload_documents(
    file: UploadFile,
    user_id: Annotated[str | None, Header()],
    session_id: Annotated[str | None, Header()],
):
    verify_user(user_db, user_id, session_id)

    file_name = file.filename
    file_content_type = file.content_type
    content = await file.read()

    doc_id = save_and_verify_docs(
        file_content_type=file_content_type, file_name=file_name, file_content=content
    )

    doc_db[user_id][doc_id] = str(file.filename)

    with open("./db/documents.json", "w") as outfile:
        json.dump(doc_db, outfile)

    return {"document_id": doc_id}


@app.post("/chat")
async def chat_llama(
    chat: Chat,
    user_id: Annotated[str | None, Header()],
    session_id: Annotated[str | None, Header()],
) -> ChatResponse:
    verify_user(user_db, user_id, session_id)

    session = client.get_or_create_session(session_id=session_id)

    query = chat.query
    response = session.run("security_layer_agent", query=query)

    if chat.document_id is not None:
        # response, reference = session.run("docs_agent", query=query, document_id=chat.document_id)
        return ChatResponse(bot_message=query, reference=query)

    if chat.agent_id == "appointment_agent":
        # response = session.run("appointment_agent", query=query)
        pass
    elif chat.agent_id == "knowledge_agent":
        # response = session.run("knowledge_agent", query=query)
        pass
    else:
        # response = session.run("multi_agent", query=query)
        pass

    return ChatResponse(bot_message=response)
