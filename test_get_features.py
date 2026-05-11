import pytest

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.callbacks.base import BaseCallbackHandler
from config import MODEL_NAME, SYSTEM_PROMPT, get_mcp_client

USER_INPUT = "Donne-moi les bâtiments de la BDTOPO proches du point longitude 6.87, latitude 45.92 (Chamonix)."


class ToolCallTracker(BaseCallbackHandler):
    def __init__(self):
        self.tool_calls = []

    def on_tool_start(self, serialized, input_str, **kwargs):
        self.tool_calls.append({"name": serialized.get("name", "unknown"), "type": "start"})


@pytest.mark.asyncio
async def test_get_features():
    client = get_mcp_client()
    tools = await client.get_tools()

    get_features_tool = next((t for t in tools if t.name == "gpf_wfs_get_features"), None)
    assert get_features_tool is not None, "Tool 'gpf_wfs_get_features' not found"

    model = init_chat_model(MODEL_NAME, temperature=0.0)
    agent = create_agent(model=model, tools=tools, system_prompt=SYSTEM_PROMPT)
    assert agent is not None

    tracker = ToolCallTracker()
    result = await agent.ainvoke(
        {"messages": [{"role": "user", "content": USER_INPUT}]},
        config={"callbacks": [tracker]},
    )

    wfs_calls = [c for c in tracker.tool_calls if c.get("name") in ("gpf_wfs_get_features", "gpf_wfs_search_types")]
    assert len(wfs_calls) > 0, "No WFS tool was called"

    last_message = result["messages"][-1]
    message_text = str(last_message).lower()

    assert "bâtiment" in message_text or "batiment" in message_text or "bdtopo" in message_text
