import asyncio
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

load_dotenv()

llm = ChatOpenAI()

async def main():
    print("Starting MCP client...")
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                # Make sure to update to the full absolute path to your math_server.py file
                "args": ["D:\\github\\mcps\\lc\\mcp-crash-course\\servers\\math_server.py"],
                "transport": "stdio",
            },
            "weather": {
                # make sure you start your weather server on port 8000
                "url": "http://localhost:8000/mcp",
                "transport": "streamable_http",
            }
        }
    ) 
    agent = create_react_agent(llm, await client.get_tools())
    result = await agent.ainvoke({"messages": "what's (3 + 5) x 10?"})
    print(result["messages"][-1].content)
    result2 = await agent.ainvoke({"messages": "whatS the weather in Dubai?"})
    print(result2["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
