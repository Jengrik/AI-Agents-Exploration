import asyncio
from agents.test_agent import TestAgent

async def main():
  #* Initialize the agent
  agent = TestAgent()

  question = "What's the difference between hiking and trekking?"
  response = await agent.ask_question(question)

  #* Logs
  print(f"Question: {question}")
  print(f"Response: {response}")

if __name__ == "__main__":
    asyncio.run(main())
