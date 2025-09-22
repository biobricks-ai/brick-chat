import chainlit as cl


@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="List bricks",
            message="Get me a list of bricks with their descriptions",
        ),
        cl.Starter(
            label="Find human genome bricks",
            message="Get me a list of bricks discussing the human genome",
        ),
        cl.Starter(
            label="Clinical variations information",
            message="I want some information on clinical variations, so find me a brick that will handle that",
        ),
    ]
