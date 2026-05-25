import os
from fastapi import APIRouter
from datetime import datetime
from rag.ingest import delete_document_vectors
from rag.bm25_store import remove_document_from_bm25
router = APIRouter()

UPLOAD_DIR = "uploads"

@router.get("/documents")
async def get_document():
    documents = []

    if os.path.exists(UPLOAD_DIR):
        for filename in os.listdir(UPLOAD_DIR):
            file_path = os.path.join(UPLOAD_DIR,filename)
            if os.path.isfile(file_path):
                stat = os.stat(file_path)
                documents.append({
                    "filename":filename,
                    "file_type":filename.split(".")[-1],
                    "size": round(stat.st_size/1024,2),
                    "uploaded_at":datetime.fromtimestamp(stat.st_birthtime).strftime("%Y-%m-%d %H:%M")
                })
    return{
        "documents":documents
    }

@router.delete("/documents/{filename}")
async def delete_document(
    filename: str
):

    file_path = os.path.join(
        UPLOAD_DIR,
        filename
    )

    if not os.path.exists(file_path):
        return {

            "message":
            "File not found"
        }

    os.remove(file_path)

    delete_document_vectors(filename)
    remove_document_from_bm25(filename)
    return {
        "message":
        f"{filename} deleted successfully"
    }