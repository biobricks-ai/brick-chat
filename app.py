import os

import chainlit as cl
from dotenv import load_dotenv

from google import genai
from google.genai import types
import starters

# Create a RAG Corpus, Import Files, and Generate a response

load_dotenv()


# Initialize Vertex AI API once per session
def generate(user_query: str):
    # initialize the genai client session
    client = genai.Client()

    # read the prompt and system instructions files and set up standard variables for the model
    with open("instructions/prompt.md", "r", encoding="utf-8") as f:
        prompt_template = f.read()
    with open("instructions/si.md", "r", encoding="utf-8") as f:
        si = f.read()
    msg = types.Part.from_text(
        text=prompt_template.format(
            user_query=user_query, brick_name="Ex. 1000 Genomes is 1000_genomes"
        )
    )
    model = "gemini-2.5-flash-lite"
    contents = [
        types.Content(role="user", parts=[msg]),
    ]

    # Create a RAG retrieval tool
    rag_retrieval_tool = [
        types.Tool(
            retrieval=types.Retrieval(
                vertex_rag_store=types.VertexRagStore(
                    rag_resources=[
                        types.VertexRagStoreRagResource(
                            rag_corpus=os.getenv("CORPUS_NAME")
                        )
                    ],
                    similarity_top_k=20,
                ),
            )
        )
    ]

    # setup the model generation configuration
    temperature = 0.8
    top_p = 0.5
    max_output_tokens = 65535  # maximum possible for this model
    # Low threshold safety
    thinking = 0  # Thinking: OFF
    generate_content_config = types.GenerateContentConfig(
        temperature=temperature,
        top_p=top_p,
        max_output_tokens=max_output_tokens,
        safety_settings=[
            types.SafetySetting(
                category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_LOW_AND_ABOVE"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="BLOCK_LOW_AND_ABOVE",
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                threshold="BLOCK_LOW_AND_ABOVE",
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_LOW_AND_ABOVE"
            ),
        ],
        tools=rag_retrieval_tool,
        system_instruction=[types.Part.from_text(text=si)],
        thinking_config=types.ThinkingConfig(
            thinking_budget=thinking,
        ),
    )

    # use a content stream to gather the output from the model and return the collected stream
    for chunk in client.models.generate_content_stream(
        model=model, contents=contents, config=generate_content_config
    ):
        if (
            not chunk.candidates
            or not chunk.candidates[0].content
            or not chunk.candidates[0].content.parts
        ):
            continue
        yield chunk.text


@cl.on_message
async def main(message: cl.Message):
    # Create a message placeholder
    msg = await cl.Message(content="").send()

    # Stream chunks from the model
    for chunk in generate(message.content):
        await msg.stream_token(chunk)

    # Finalize
    await msg.update()
