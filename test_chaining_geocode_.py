import pytest
import re

from langchain.agents import create_agent
from config import MODEL_NAME, get_mcp_client

@pytest.mark.asyncio
async def test_chaining_geocode_altitude():
    client = get_mcp_client()
    tools = await client.get_tools()

    agent = create_agent(MODEL_NAME,tools=tools, 
        system_prompt="You are a helpful assistant for geospatial data. You can use the following tools to answer questions about geospatial data: {tools}. Always use these tools when relevant to answer the user's question."
    )
    assert agent is not None

    question = "Quelle est l'altitude de la mairie de Chamonix?"
    result = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})

    last_message = result["messages"][-1]
    message_text = str(last_message).replace("\u202f", " ").replace("\xa0", " ")

    print(last_message.pretty_print())
    assert "chamonix" in message_text.lower()
    # ensure that the altitude is around 1036m, allowing for some variation in the response format
    assert re.search(r"\b1\s*036\b", message_text)
