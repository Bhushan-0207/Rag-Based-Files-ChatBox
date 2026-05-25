from rank_bm25 import BM25Okapi

bm25_docs = []

bm25_corpus = []

tokenized_docs = []

bm25 = None


def build_bm25(chunks):

    global bm25

    for chunk in chunks:

        bm25_docs.append(chunk)

        bm25_corpus.append(
            chunk.page_content
        )

    tokenized_docs.clear()

    for text in bm25_corpus:

        tokenized_docs.append(
            text.split()
        )

    bm25 = BM25Okapi(tokenized_docs)
    print(f"BM25 Indexed: {len(bm25_docs)} chunks")


def remove_document_from_bm25(filename):

    global bm25
    global bm25_docs
    global bm25_corpus

    updated_docs = []

    for doc in bm25_docs:

        if (
            doc.metadata.get(
                "source"
            ) != filename
        ):

            updated_docs.append(doc)

    bm25_docs = updated_docs

    bm25_corpus = [

        doc.page_content

        for doc in bm25_docs
    ]

    tokenized_docs = [

        text.split()

        for text in bm25_corpus
    ]

    if len(tokenized_docs) > 0:

        bm25 = BM25Okapi(
        tokenized_docs
    )

    else:

        bm25 = None