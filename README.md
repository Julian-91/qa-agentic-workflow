# QA Agentic Workflow

This project is a proof-of-concept for an agentic QA workflow with multiple AI agents that autonomously perform QA tasks (such as accessibility scans, security scans, and test design) on an application, orchestrated via LangGraph workflows and MCP tooling.

## Features
- Modular agent architecture with LangGraph
- Integration with Playwright MCP server for accessibility and security scans
- GitHub agent that fetches code changes from a specific pull request and a specific issue
- Test design agent that generates test cases from the PR diff and the issue description
- Use of LLMs (OpenAI, Anthropic, etc.) as reasoning engine
- Easily extensible with extra agents/tools

## Installation
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Ensure Node.js and npx are installed** (for Playwright MCP and GitHub MCP servers)
3. **Create a `.env` file** with your API keys, for example:
   ```env
   OPENAI_API_KEY=sk-...yourtoken...
   GITHUB_PERSONAL_ACCESS_TOKEN=ghp_...yourgithubtoken...
   ```

## Usage
1. **Start the workflow:**
   ```bash
   python main.py
   ```
2. **Result:**
   The workflow performs various QA tasks through agents and prints the result to the console.

## Structure
- `main.py`: Entry point and workflow definition
- `state.py`: State definitions for the workflow
- `agents/`: Directory with agent nodes (accessibility_scan, security_scan, github_agent, test_design, ...)

## Extending
- Add extra agents in the `agents/` folder
- Extend the state in `state.py`
- Add nodes to the workflow in `main.py`