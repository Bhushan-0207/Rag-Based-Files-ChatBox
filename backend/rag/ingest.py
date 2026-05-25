import uuid
import os
from datetime import datetime

from services.parse_service import extract_text
from rag.bm25_store import build_bm25
from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# EMBEDDINGS
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# SEMANTIC CHUNKER
text_splitter = SemanticChunker(
    embeddings
)

# CHROMA DB
vector_db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)


def ingest_document(file_path):

    parsed_docs = extract_text(file_path)

    all_chunks = []

    filename = os.path.basename(file_path)

    file_extension = filename.split(".")[-1]

    for parsed_doc in parsed_docs:

        content = parsed_doc["content"]

        metadata = parsed_doc["metadata"]

        # Semantic Chunking
        chunks = text_splitter.create_documents(
            [content]
        )

        for chunk in chunks:

            final_metadata = {

                
                "document_id": str(uuid.uuid4()),
                "source": filename,
                "file_path": file_path,
                "file_type": file_extension,

            
                "chunk_id": str(uuid.uuid4()),

                
                "uploaded_at": str(datetime.utcnow()),

                
                **metadata
            }

            chunk.metadata = final_metadata

            all_chunks.append(chunk)

    
    vector_db.add_documents(all_chunks)


    build_bm25(all_chunks)

    print(f"\nStored {len(all_chunks)} chunks")

    return all_chunks

def delete_document_vectors(filename):

    vector_db.delete(
        where={
            "source":filename
        }
    )

