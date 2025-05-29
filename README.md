# QA Agentic Workflow

This project is a proof-of-concept for an agentic QA workflow with multiple AI agents that autonomously perform QA tasks (such as accessibility scans) on an application, orchestrated via LangGraph workflows and MCP tooling.

## Features
- Modular agent architecture with LangGraph
- Integration with Playwright MCP server for accessibility scans
- Use of LLMs (OpenAI, Anthropic, etc.) as reasoning engine
- Easily extensible with extra agents/tools

## Installation
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Ensure Node.js and npx are installed** (for Playwright MCP server)
3. **Create a `.env` file** with your LLM API key, for example:
   ```env
   OPENAI_API_KEY=sk-...yourtoken...
   ```

## Usage
1. **Start the workflow:**
   ```bash
   python main.py
   ```
2. **Result:**
   The workflow performs an accessibility scan on the specified URL and prints the result to the console.

## Structure
- `main.py` — Entry point, defines the workflow
- `state.py` — TypedDict for the workflow state
- `agents/accessibility_scan.py` — Agent node for accessibility scans via MCP/Playwright
- `requirements.txt` — Python dependencies
- `.env` — (not in git) Contains your API keys

## Extending
- Add extra agents in the `agents/` folder
- Extend the state in `state.py`
- Add nodes to the workflow in `main.py`

## License
MIT 