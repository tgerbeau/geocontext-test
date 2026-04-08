import pytest

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from config import MODEL_NAME, SYSTEM_PROMPT, get_mcp_client

USER_INPUT = "Dans quelle table peut-on trouver des informations sur les écoles?"

@pytest.mark.asyncio
async def test_search_ecoles():
    client = get_mcp_client()
    tools = await client.get_tools()

    model = init_chat_model(MODEL_NAME,temperature=0.0)
    agent = create_agent(
        model=model,
        tools=tools, 
        system_prompt=SYSTEM_PROMPT
    )
    assert agent is not None
    
    result = await agent.ainvoke({"messages": [{"role": "user", "content": USER_INPUT}]})

    last_message = result["messages"][-1]
    message_text = str(last_message)

    assert "ERP" in message_text

