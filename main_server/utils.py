import random
import string
import json
from typing import Dict
from fastapi import HTTPException, status

# from llama_index.readers.file import PDFReader, DocxReader # , PptxReader
import os

# pdf_reader = PDFReader()
# docx_reader = DocxReader()
# pptx_reader = PptxReader()


def generate_unique_id(length: int = 7) -> str:
    characters = string.ascii_letters + string.digits
    unique_id = "".join(random.choice(characters) for _ in range(length))

    return unique_id


def save_and_verify_docs(file_content_type: str, file_name: str, file_content) -> str:
    if file_content_type not in [
        "application/json",
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.ms-powerpoint",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ]:
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF, DOC, DOCX, PPT or PPTX file !!!",
        )

    file_location = f"/home/rion/agents/PS4-Context-Crafters/s3_bucket/{file_name}"

    doc_id = generate_unique_id()

    os.makedirs(os.path.dirname(file_location), exist_ok=True)

    # with open(file_location, "wb") as f:
    #     f.write(file_content)
    #
    # if file_content_type in ["application/pdf"]:
    #     try:
    #         doc = pdf_reader.load_data(file_location)
    #     except:
    #         os.remove(file_location)
    #         raise HTTPException(status_code=400, detail="Couldn't read the PDF !!!")
    #
    # elif file_content_type in ["application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
    #     try:
    #         doc = docx_reader.load_data(file_location)
    #     except:
    #         os.remove(file_location)
    #         raise HTTPException(status_code=400, detail="Couldn't read the DOC or DOCX !!!")

    # elif file_content_type in ["application/vnd.ms-powerpoint", "application/vnd.openxmlformats-officedocument.presentationml.presentation"]:
    #     try:
    #         doc = pptx_reader.load_data(file_location)
    #     except:
    #         raise HTTPException(status_code=400, detail="Couldn't read the PPT or PPTX !!!")

    return doc_id

