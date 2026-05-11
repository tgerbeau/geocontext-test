import pytest

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.callbacks.base import BaseCallbackHandler
from config import MODEL_NAME, SYSTEM_PROMPT, get_mcp_client

USER_INPUT = "Y a-t-il des servitudes d'utilité publique au 10 place Bellecour, Lyon?"


class ToolCallTracker(BaseCallbackHandler):
    def __init__(self):
        self.tool_calls = []

    def on_tool_start(self, serialized, input_str, **kwargs):
        self.tool_calls.append({"name": serialized.get("name", "unknown"), "type": "start"})


@pytest.mark.asyncio
async def test_chaining_geocode_assiette_sup():
    """Test chaining: geocode -> assiette_sup.

    The agent should geocode the address first, then use assiette_sup
    to look up servitudes d'utilité publique at those coordinates.
    """
    client = get_mcp_client()
    tools = await client.get_tools()

    model = init_chat_model(MODEL_NAME, temperature=0.0)
    agent = create_agent(model=model, tools=tools, system_prompt=SYSTEM_PROMPT)
    assert agent is not None

    tracker = ToolCallTracker()
    result = await agent.ainvoke(
        {"messages": [{"role": "user", "content": USER_INPUT}]},
        config={"callbacks": [tracker]},
    )

    tool_names_called = {c.get("name") for c in tracker.tool_calls if c.get("type") == "start"}

    assert "geocode" in tool_names_called, "geocode tool was not called"
    assert "assiette_sup" in tool_names_called, "assiette_sup tool was not called"

    last_message = result["messages"][-1]
    message_text = str(last_message).lower()

    keywords = ["servitude", "assiette", "sup", "bellecour", "lyon", "utilité publique"]
    assert any(k in message_text for k in keywords), \
        f"None of {keywords} found in response"
