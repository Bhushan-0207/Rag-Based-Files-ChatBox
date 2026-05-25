import os
import shutil

from fastapi import (
    APIRouter,
    UploadFile,
    File
)

from rag.ingest import (
    ingest_document
)


router = APIRouter()

UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


@router.post("/upload")
async def upload_files(
    files: list[UploadFile] = File(...)
):

    uploaded_files = []

    for file in files:

        file_path = os.path.join(
            UPLOAD_DIR,
            file.filename
        )

        with open(file_path, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        # INGEST INTO RAG
        chunks = ingest_document(
            file_path
        )

        uploaded_files.append({

            "filename":
            file.filename,

            "chunks":
            len(chunks)
        })

    return {

        "message":
        "Files uploaded successfully",

        "files":
        uploaded_files
    }