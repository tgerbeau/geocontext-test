import pytest

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.callbacks.base import BaseCallbackHandler
from config import MODEL_NAME, SYSTEM_PROMPT, get_mcp_client

USER_INPUT = "Quels sont les attributs de la table BDTOPO_V3:batiment?"


class ToolCallTracker(BaseCallbackHandler):
    def __init__(self):
        self.tool_calls = []

    def on_tool_start(self, serialized, input_str, **kwargs):
        self.tool_calls.append({"name": serialized.get("name", "unknown"), "type": "start"})


@pytest.mark.asyncio
async def test_describe_type():
    client = get_mcp_client()
    tools = await client.get_tools()

    describe_tool = next((t for t in tools if t.name == "gpf_wfs_describe_type"), None)
    assert describe_tool is not None, "Tool 'gpf_wfs_describe_type' not found"

    model = init_chat_model(MODEL_NAME, temperature=0.0)
    agent = create_agent(model=model, tools=tools, system_prompt=SYSTEM_PROMPT)
    assert agent is not None

    tracker = ToolCallTracker()
    result = await agent.ainvoke(
        {"messages": [{"role": "user", "content": USER_INPUT}]},
        config={"callbacks": [tracker]},
    )

    describe_calls = [c for c in tracker.tool_calls if c.get("name") == "gpf_wfs_describe_type"]
    assert len(describe_calls) > 0, "gpf_wfs_describe_type tool was not called"

    last_message = result["messages"][-1]
    message_text = str(last_message).lower()

    assert "geometrie" in message_text or "geometry" in message_text or "hauteur" in message_text
