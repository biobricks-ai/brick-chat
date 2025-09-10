import os

import chainlit as cl
from dotenv import load_dotenv

from google import genai
from google.genai import types

# Create a RAG Corpus, Import Files, and Generate a response

load_dotenv()


# Initialize Vertex AI API once per session
def generate(user_query: str):
    # initialize the genai client session
    client = genai.Client()

    # read the prompt and system instructions files and set up standard variables for the model
    with open("instructions/prompt.txt", "r", encoding="utf-8") as f:
        prompt_template = f.read()
    with open("instructions/si.txt", "r", encoding="utf-8") as f:
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
    # Temperature: 1
    # Top P: 0.95
    # Maximum Output Tokens: 65535 (maximum possible for this model)
    # Default safety options
    # Thinking: OFF
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        max_output_tokens=65535,
        safety_settings=[
            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
            types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"
            ),
            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF"),
        ],
        tools=rag_retrieval_tool,
        system_instruction=[types.Part.from_text(text=si)],
        thinking_config=types.ThinkingConfig(
            thinking_budget=0,
        ),
    )

    # use a content stream to gather the output from the model and return the collected stream
    response_chunks = []
    for chunk in client.models.generate_content_stream(
        model=model, contents=contents, config=generate_content_config
    ):
        if (
            not chunk.candidates
            or not chunk.candidates[0].content
            or not chunk.candidates[0].content.parts
        ):
            continue
        response_chunks.append(chunk.text)
    response = "".join(response_chunks)

    return response


@cl.on_message
async def main(message: cl.Message):
    # Generate response
    response = generate(message.content)

    # Send a response back to the user
    await cl.Message(content=response).send()
