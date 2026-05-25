import os

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI


load_dotenv()

api_key = os.getenv("API_KEY")


llm = ChatOpenAI(
    model="openai/gpt-oss-120b:free",
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)


def format_context(compressed_results):

    context_parts = []

    for item in compressed_results:

        metadata = item["metadata"]

        source = metadata.get(
            "source",
            "Unknown"
        )

        chunk_id = metadata.get(
            "chunk_id",
            "N/A"
        )

        location = ""

        if "page" in metadata:

            location = f"Page {metadata['page']}"

        elif "slide" in metadata:

            location = f"Slide {metadata['slide']}"

        elif "sheet" in metadata:

            location = f"Sheet {metadata['sheet']}"

        context_parts.append(
            f"""
CONTENT:
{item['sentence']}

SOURCE:
{source}

LOCATION:
{location}

CHUNK_ID:
{chunk_id}
"""
        )

    return "\n\n".join(context_parts)




def generate_answer(
    query,
    compressed_results
):

    context = format_context(
        compressed_results
    )

    prompt = f"""
You are a strict AI document assistant.

Answer ONLY using the provided context.

Do NOT use external knowledge.

If answer is not available in context say:
"I don't know based on the uploaded documents."

Always provide citations.

Use this citation format:

(Source: filename, Location: page/slide/sheet)

CONTEXT:
{context}

QUESTION:
{query}

ANSWER:
"""

    response = llm.invoke(prompt)

    return response.content




def stream_answer(
    query,
    compressed_results
):

    context = format_context(
        compressed_results
    )

    prompt = f"""
You are a strict AI document assistant.

Answer ONLY using the provided context.

Do NOT use external knowledge.

If the answer is not present in the context say:

"I don't know based on the uploaded documents."

Provide a clean and concise answer.

Do NOT generate citations yourself.

Context:
{context}

Question:
{query}

Answer:
"""

    streaming_llm = ChatOpenAI(
        model="openai/gpt-oss-120b:free",
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        streaming=True
    )

    for chunk in streaming_llm.stream(prompt):

        if chunk.content:

            yield chunk.content