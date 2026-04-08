import asyncio

from langchain.agents import create_agent
from config import MODEL_NAME


def test_agent_creation_call_and_paris_in_response():
	agent = create_agent(MODEL_NAME)

	assert agent is not None

	question = "Quelle est la capitale de la France"
	response = asyncio.run(
		agent.ainvoke({"messages": [{"role": "user", "content": question}]})
	)

	assert "paris" in str(response).lower()
