import re


def split_sentences(text):

    sentences = re.split(
        r'(?<=[.!?])\s+',
        text
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def compress_context(
    ranked_results,
    query,
    reranker,
    top_sentences=3
):
    if len(ranked_results) == 0:
        return []
    
    compressed_results = []

    for item in ranked_results:

        doc = item["document"]

        score = item["score"]

        # Split chunk into sentences
        sentences = split_sentences(
            doc.page_content
        )

        if not sentences:
            continue

        # Query-sentence pairs
        sentence_pairs = []

        for sentence in sentences:

            sentence_pairs.append([
                query,
                sentence
            ])

        # Score sentences
        sentence_scores = reranker.predict(
            sentence_pairs
        )

        # Rank sentences
        ranked_sentences = sorted(
            zip(sentences, sentence_scores),
            key=lambda x: x[1],
            reverse=True
        )

        # Select top sentences
        best_sentences = ranked_sentences[
            :top_sentences
        ]

        # Store compressed output
        for sentence, sentence_score in best_sentences:

            compressed_results.append({

                "sentence": sentence,

                "sentence_score": float(
                    sentence_score
                ),

                "document_score": score,

                "metadata": doc.metadata
            })

    # Final ranking
    compressed_results = sorted(
        compressed_results,
        key=lambda x: x["sentence_score"],
        reverse=True
    )

    return compressed_results
