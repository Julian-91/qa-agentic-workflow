# QA Agentic Workflow

This project is a proof-of-concept for an agentic QA workflow with multiple AI agents that autonomously perform QA tasks (such as accessibility scans, security scans, and test design) on an application, orchestrated via LangGraph workflows and MCP tooling.

## Features
- Modular agent architecture with LangGraph
- **Dynamic agent selection**: The `assign_worker` agent determines which QA agents (UI, accessibility, security, etc.) should run for a given PR/issue.
- **Conditional workflow routing**: Only the agents selected by `assign_worker` are executed, using conditional edges in the workflow.
- **Grouped test cases per agent**: The test design agent generates test cases only for the selected agents, and these are stored in separate lists in the state (e.g., `testcases_ui_test`, `testcases_accessibility_test`, `testcases_security_test`).
- Integration with Playwright MCP server for accessibility and security scans
- GitHub agent that fetches code changes from a specific pull request and a specific issue
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
   python ui_check_workflow.py
   ```
2. **Result:**
   The workflow performs various QA tasks through agents and prints the result to the console. Only the agents selected by the `assign_worker` agent will run for each workflow execution.

## Structure
- `ui_check_workflow.py`: Main workflow definition and entry point
- `states.py`: State definitions for the workflow (TypedDicts)
- `agents/`: Directory with agent nodes (accessibility_scan, security_scan, github_agent, test_design, assign_worker, ...)

## Extending
- Add extra agents in the `agents/` folder
- Extend the state in `states.py`
- Add nodes to the workflow in `ui_check_workflow.py`