from rag.ingest import vector_db

import rag.bm25_store as bm25_store



def vector_search(
    query,
    filters=None,
    k=5
):

    if filters and filters.get("sources"):
        source_filters = {

        "$or": [

            {"source": source}

            for source in
            filters["sources"]
            ]
        }

        results = vector_db.similarity_search(
            query,
            k=k,
            filter=source_filters
        )


    else:

        results = vector_db.similarity_search(
            query,
            k=k
        )

    return results

def bm25_search(
    query,
    filters=None,
    n=5
):

    if bm25_store.bm25 is None:
        return []

    if bm25_store.bm25 is not None:

        bm25_text_results = bm25_store.bm25.get_top_n(
            query.split(),
            bm25_store.bm25_corpus,
            n=n
        )

    else:

        bm25_text_results = []

    bm25_results = []

    for text in bm25_text_results:

        for doc in bm25_store.bm25_docs:

            if doc.page_content == text:

                # METADATA FILTERING
                if filters:

                    matched = True

                    for key, value in filters.items():

                        if doc.metadata.get(key) != value:

                            matched = False
                            break

                    if not matched:
                        continue

                bm25_results.append(doc)

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