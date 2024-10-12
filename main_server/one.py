from collections.abc import Collection
import llama_index
from llama_index.llms.ollama import Ollama
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SemanticSplitterNodeParser, SentenceSplitter
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core import Settings

# from llama_index.embeddings.google import GooglePaLMEmbedding
# from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
# from llama_index.core.query_engine import

import qdrant_client
from qdrant_client.models import Distance, VectorParams

# data = SimpleDirectoryReader(input_files=["./data/sample.json"]).load_data()
data = SimpleDirectoryReader(input_files=["./data/maxlife.pdf"]).load_data()
# splitter = SemanticSplitterNodeParser(
#     buffer_size=1, breakpoint_percentile_threshold=50, embed_model=embed_model
# )
# nodes = splitter.get_nodes_from_documents(data)
# print(len(nodes))
client = qdrant_client.QdrantClient(location=":memory:")
client = qdrant_client.QdrantClient(host="localhost", port=6333)
# client.create_collection(
#     collection_name="test_store",
#     vectors_config=VectorParams(size=384, distance=Distance.DOT),
# )
# vector_store = QdrantVectorStore(client=client, collection_name="test_store")
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
llm = Ollama(model="gemma2:2b-text-q8_0", request_timeout=120)
Settings.embed_model = embed_model
Settings.llm = llm
pipeline = IngestionPipeline(
    transformations=[
        SemanticSplitterNodeParser(
            buffer_size=2, breakpoint_percentile_threshold=30, embed_model=embed_model
        ),
        # SentenceSplitter(chunk_size=25, chunk_overlap=0),
        # embed_model,
    ],
    # vector_store=vector_store,
)
nodes = pipeline.run(data)
# index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
# storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    nodes,
    # storage_context=storage_context,
)
query_index = index.as_query_engine(
    summarize_mode="tree_summarize", verbose=True, llm=llm
)

response = query_index.query("What is the price of smart thermostat")
print(response)
