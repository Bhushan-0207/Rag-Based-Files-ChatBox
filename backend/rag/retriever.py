from rag.ingest import vector_db

import rag.bm25_store as bm25_store



def vector_search(
    query,
    filters=None,
    k=5
):

    if (filters and filters.get("sources")):

        selected_sources = (
            filters["sources"]
        )

        vector_results = []

        for source in selected_sources:

            results = (
                vector_db.similarity_search(

                    query,

                    k=k,

                    filter={
                        "source": source
                    }
                )
            )

            vector_results.extend(
                results
            )
    else:

        vector_results = (
            vector_db.similarity_search(
                query,
                k=k
            )
        )

    return vector_results

def bm25_search(
    query,
    filters=None,
    n=5
):

    if bm25_store.bm25 is None:
        return []

    # FILTERED DOCS
    filtered_bm25_docs = (
        bm25_store.bm25_docs
    )

    if (
        filters
        and
        filters.get("sources")
    ):

        filtered_bm25_docs = [

            doc

            for doc in
            bm25_store.bm25_docs

            if doc.metadata.get(
                "source"
            ) in filters["sources"]
        ]

    filtered_corpus = [

        doc.page_content

        for doc in
        filtered_bm25_docs
    ]

    # EMPTY FILTERED CORPUS
    if len(filtered_corpus) == 0:
        return []

    bm25_text_results = (
        bm25_store.bm25.get_top_n(

            query.split(),

            filtered_corpus,

            n=n
        )
    )

    bm25_results = []

    for text in bm25_text_results:

        for doc in filtered_bm25_docs:

            if doc.page_content == text:

                bm25_results.append(
                    doc
                )

                break

    return bm25_results


def hybrid_merge(vector_results, bm25_results):

    combined_results = []

    combined_results.extend(vector_results)

    combined_results.extend(bm25_results)

    # Remove duplicates
    unique_docs = {}

    for doc in combined_results:

        unique_docs[doc.page_content] = doc

    return list(unique_docs.values())


def retrieve_documents(
    query,
    filters=None
):

    vector_results = vector_search(
        query,
        filters
    )

    bm25_results = bm25_search(
        query,
        filters
    )

    combined_results = hybrid_merge(
        vector_results,
        bm25_results
    )
    if len(combined_results) == 0:

        return []

    return combined_results 