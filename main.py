import asyncio
from langchain.agents import create_agent
from config import MODEL_NAME

agent = create_agent(MODEL_NAME)

async def main() -> None:
	result = await agent.ainvoke(
		{"messages": [{"role": "user", "content": "What is the capital of France?"}]}
	)
	print(result)


if __name__ == "__main__":
	asyncio.run(main())


