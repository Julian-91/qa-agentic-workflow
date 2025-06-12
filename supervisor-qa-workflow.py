from langchain_openai import ChatOpenAI

from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()


github_mcp_client = MultiServerMCPClient({
   "github": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "GITHUB_PERSONAL_ACCESS_TOKEN",
        "ghcr.io/github/github-mcp-server"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
      },
      "transport": "stdio",
    }
})

playwright_mcp_client = MultiServerMCPClient({
    "playwright": {
        "command": "npx",
        "args": [
            "@playwright/mcp@latest"
        ],
        "transport": "stdio"
    }
})

async def get_github_tool():
    return await github_mcp_client.get_tools()

async def get_playwright_tool():
    return await playwright_mcp_client.get_tools()

github_tool = asyncio.run(get_github_tool())
playwright_tool = asyncio.run(get_playwright_tool())

model = ChatOpenAI(model="gpt-4o")


github_agent = create_react_agent(
    model=model,
    tools=github_tool,
    name="github_data_retriever",
    prompt="You are a github data retriever.You call the github tool to get the code diff from a pull request by pull request number first and then the issue content from a github issue by issue number. You will be given a repository, a pull request number and an issue number."
)

test_design_agent = create_react_agent(
    model=model,
    tools=[],
    name="test_design_expert",
    prompt="You are a world class test designer. You design test cases based on the code diff from a pull request and the issue content from a github issue."
)

ui_test_agent = create_react_agent(
    model=model,
    tools=playwright_tool,
    name="ui_test_expert",
    prompt="You are a world class ui test expert. You test the ui of a web application and return the results. You will be given a url and a list of test cases. You will use the playwright tool to test the ui."
)

# Create supervisor workflow
workflow = create_supervisor(
    [github_agent, test_design_agent, ui_test_agent],
    model=model,
    prompt=(
        "You are a supervisor agent managing a GitHub data retriever, a test design expert and a ui test expert. "
        "For retrieving information from GitHub (such as pull request diffs or issue content), delegate to the github_data_retriever agent. This agent will require a repository, a pull request number and an issue number. "
        "For queries about designing test cases based on code changes or issues, delegate to the test_design_expert agent. This agent will require the code diff from a pull request and the issue content from a github issue. "
        "For executing functional tests on a ui of a web application, delegate to the ui_test_expert agent. This agent will require a url and a list of test cases to execute. "
        "Coordinate the agents as needed to answer complex queries that require both retrieving GitHub data, designing tests and executing functional tests on a ui of a web application. "
        "Always explain your reasoning and ensure each agent is used for its area of expertise."
    )
)

# Compile and run
app = workflow.compile()
result = asyncio.run(app.ainvoke({
    "messages": [
        {
            "role": "user",
            "content": "Execute ui tests for the following pull request #20, issue #19 in the repository https://github.com/Julian-91/angular-todo-app. The url of the web application to test is http://localhost:4200/add"
        }
    ]
}))
print(result)