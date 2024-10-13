from pathlib import Path
from huggingface_hub.file_download import uuid
import llama_index
from llama_index.core.ingestion import IngestionPipeline
from llama_index.llms.ollama import Ollama
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    Settings,
    StorageContext,
)
from llama_index.core.node_parser import SimpleFileNodeParser
from llama_index.core.readers.file import FlatReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import qdrant_client
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client.models import VectorParams, Distance

embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
llm = Ollama(model="gemma:2b-text-q8_0")
Settings.llm = llm
Settings.embed_model = embed_model


client = qdrant_client.QdrantClient(host="localhost", port=6333)


def load_doc(mobile: str, doc_loc: str):
    if not client.collection_exists(mobile):
        client.create_collection(
            collection_name=mobile,
            vectors_config=VectorParams(distance=Distance.DOT, size=384),
        )

    parent_vdb = QdrantVectorStore(collection_name=mobile)
    parent_context = StorageContext.from_defaults(vector_store=parent_vdb)
    doc_id = uuid.uuid4()
    collection_name = mobile + "_" + str(doc_id)
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(distance=Distance.DOT, size=384),
    )
    child_vdb = QdrantVectorStore(collection_name=collection_name)
    child_context = StorageContext.from_defaults(vector_store=child_vdb)

    docs = FlatReader().load_data(Path(doc_loc))
    nodes = SimpleFileNodeParser().get_nodes_from_documents(docs)
    pipeline = IngestionPipeline(transformations=[embed_model])
    nodes = pipeline.run(nodes)

    VectorStoreIndex(nodes, storage_context=parent_context)
    VectorStoreIndex(nodes, storage_context=child_context)

    return str(doc_id)


# def query(query: str, mobile:str, doc_id:str):
def query(*args):
    if len(args) == 2:
        query, mobile = args
        collection_name = mobile
    else:
        query, mobile, doc_id = args
        collection_name = mobile + "_" + doc_id

    vector_store = QdrantVectorStore(collection_name=collection_name)
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    query_engine = index.as_query_engine(llm, response_mode="refined")
    response = query_engine.query(query)

    return response


# def query(query:str, mobile:str):
#     vector_store = QdrantVectorStore(collection_name=mobile)
#     index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
#     query_engine = index.as_query_engine(llm, response_mode="refined")
#     response = query_engine.query(query)

#     return response
