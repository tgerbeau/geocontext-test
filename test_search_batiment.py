import pytest
import re

from langchain.agents import create_agent
from config import MODEL_NAME, get_mcp_client

@pytest.mark.asyncio
async def test_chaining_geocode_altitude():
    client = get_mcp_client()
    tools = await client.get_tools()

    agent = create_agent(MODEL_NAME,tools=tools)
    assert agent is not None

    question = "Dans quelle table peut-on trouver des informations sur les bâtiments?"
    result = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})

    last_message = result["messages"][-1]
    message_text = str(last_message)

    print(last_message.pretty_print())

    assert "BDTOPO_V3:batiment" in message_text
    assert "CADASTRALPARCELS.PARCELLAIRE_EXPRESS:batiment" in message_text

