from retriever import retrieve_documents
from reranker import rerank_documents

docs = retrieve_documents(
    "How to maintain cholesterol?"
)

ranked = rerank_documents(
    "How to maintain cholesterol?",
    docs
)

for item in ranked:

    print("\nSCORE:")
    print(item["score"])

    print("\nCONTENT:")
    print(item["document"].page_content[:300])

    print("\nMETADATA:")
    print(item["document"].metadata)

    print("=" * 80)