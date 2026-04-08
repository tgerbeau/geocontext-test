import asyncio

from langchain.agents import create_agent
from config import MODEL_NAME

USER_INPUT = "Quelle est la capitale de la France"

def test_agent_creation_call_and_paris_in_response():
	agent = create_agent(MODEL_NAME)

	assert agent is not None

	response = asyncio.run(
		agent.ainvoke({"messages": [{"role": "user", "content": USER_INPUT}]})
	)

	assert "paris" in str(response).lower()
