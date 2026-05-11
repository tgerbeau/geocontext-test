import pytest

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.callbacks.base import BaseCallbackHandler
from config import MODEL_NAME, SYSTEM_PROMPT, get_mcp_client

USER_INPUT = "Dans quelle table peut-on trouver des informations sur les bâtiments?"


class ToolCallTracker(BaseCallbackHandler):
    def __init__(self):
        self.tool_calls = []

    def on_tool_start(self, serialized, input_str, **kwargs):
        self.tool_calls.append({"name": serialized.get("name", "unknown"), "type": "start"})


@pytest.mark.asyncio
async def test_chaining_geocode_altitude():
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

    search_calls = [c for c in tracker.tool_calls if c.get("name") == "gpf_wfs_search_types"]
    assert len(search_calls) > 0, "gpf_wfs_search_types tool was not called"

    last_message = result["messages"][-1]
    message_text = str(last_message).lower()

    keywords = ["bdtopo", "batiment", "bâtiment", "parcellaire", "cadastre"]
    assert any(k in message_text for k in keywords), \
        f"None of {keywords} found in response"

