# Wiki Agent

AI research agent powered by Gemini and Wikipedia MCP. Ask a question, get sourced answers from Wikipedia via an interactive terminal dashboard.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate  # macOS/Linux

pip install -r requirements.txt
```

Create a `.env` file:

```
GOOGLE_API_KEY=your_key_here
```

## Run

```bash
python app.py
```

Type your question at the `>` prompt. Commands: `clear` (reset), `exit` (quit).

## How it works

- **LangGraph ReAct agent** loops: think, call a tool, observe result, repeat until it has an answer.
- **Gemini 2.5 Flash** is the LLM. Three Wikipedia tools: search, summary, article.
- **MCP** (Model Context Protocol) connects to a `wikipedia-mcp` server subprocess for Wikipedia API access.
- **MemorySaver** keeps conversation context within a session.

## Project structure

```
app.py                  # Terminal UI
agent/
  agent.py              # ReAct agent (LangGraph)
  tools.py              # LangChain tools wrapping MCP calls
  llm.py                # Gemini LLM instance
  memory.py             # Conversation memory
mcp_client/
  client.py             # Persistent MCP client (background thread)
prompts/
  system_prompt.py      # Agent system prompt
config.py               # API key, model name from .env
requirements.txt
```
