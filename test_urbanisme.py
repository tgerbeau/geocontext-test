import pytest

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.callbacks.base import BaseCallbackHandler
from config import MODEL_NAME, SYSTEM_PROMPT, get_mcp_client

USER_INPUT = "Quelles sont les règles d'urbanisme applicables à la parcelle 94067000AI0042?"


class ToolCallTracker(BaseCallbackHandler):
    def __init__(self):
        self.tool_calls = []

    def on_tool_start(self, serialized, input_str, **kwargs):
        self.tool_calls.append({"name": serialized.get("name", "unknown"), "type": "start"})


@pytest.mark.asyncio
async def test_urbanisme():
    client = get_mcp_client()
    tools = await client.get_tools()

    urbanisme_tool = next((t for t in tools if t.name == "urbanisme"), None)
    assert urbanisme_tool is not None, "Tool 'urbanisme' not found"

    model = init_chat_model(MODEL_NAME, temperature=0.0)
    agent = create_agent(model=model, tools=tools, system_prompt=SYSTEM_PROMPT)
    assert agent is not None

    tracker = ToolCallTracker()
    result = await agent.ainvoke(
        {"messages": [{"role": "user", "content": USER_INPUT}]},
        config={"callbacks": [tracker]},
    )

    urbanisme_calls = [c for c in tracker.tool_calls if c.get("name") == "urbanisme"]
    assert len(urbanisme_calls) > 0, "urbanisme tool was not called"

    last_message = result["messages"][-1]
    message_text = str(last_message)

    keywords = ["94067000ai0042", "urbanisme", "zone", "plu", "règle", "regle"]
    assert any(k in message_text.lower() for k in keywords), \
        f"None of {keywords} found in response"
