from sentence_transformers import CrossEncoder


reranker = CrossEncoder(
    "BAAI/bge-reranker-base"
)


def rerank_documents(
    query,
    docs,
    top_k=5
):
    if len(docs) == 0:
        return []

    if not docs:
        return []

    # Create query-doc pairs
    pairs = []

    for doc in docs:

        pairs.append([
            query,
            doc.page_content
        ])

    # Predict relevance
    scores = reranker.predict(pairs)

    # Attach scores
    scored_results = []

    for doc, score in zip(docs, scores):

        scored_results.append({
            "document": doc,
            "score": float(score)
        })

    # Sort by score
    ranked_results = sorted(
        scored_results,
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked_results[:top_k]