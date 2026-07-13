# WikiResearch AI

Terminal-based research assistant that answers questions using Wikipedia. Powered by Gemini 2.5 Flash and a persistent MCP server.

## Prerequisites

- Python 3.11+
- A Google API key ([get one here](https://aistudio.google.com/apikey))

## Setup

```bash
git clone https://github.com/RESKCORE/WIKI-Ai.git
cd WIKI-Ai
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
GOOGLE_API_KEY=your_api_key_here
```

## Usage

```bash
python app.py
```

Type your question at the `>` prompt.

| Command | Action |
|---------|--------|
| `clear` | Reset the screen |
| `exit` / `quit` | End session |
| `Ctrl+C` | Cancel current turn |

## How It Works

```
User input → LangGraph ReAct agent → Gemini 2.5 Flash (reasoning)
                                         ↓
                                    calls tool (search / summary / article)
                                         ↓
                                    Wikipedia MCP server (subprocess)
                                         ↓
                                    response rendered in terminal
```

The agent follows a ReAct loop: think, call a tool, observe the result, repeat until it has an answer. The MCP server runs as a persistent subprocess in a background thread, so every tool call reuses the same connection.

## Project Structure

```
app.py                   Terminal UI (Rich)
agent/
  agent.py               ReAct agent, LLM init, memory
  tools.py               LangChain tools wrapping MCP calls
mcp_client/
  client.py              Persistent MCP client (background thread)
prompts/
  system_prompt.py       Agent system prompt
config.py                API key and model name from .env
requirements.txt
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_API_KEY` | Yes | Google AI API key for Gemini |

## Dependencies

| Package | Purpose |
|---------|---------|
| `langchain` | Tool framework |
| `langchain-google-genai` | Gemini LLM integration |
| `langgraph` | ReAct agent loop + conversation memory |
| `mcp` | Model Context Protocol client |
| `python-dotenv` | Load `.env` files |
| `rich` | Terminal formatting (panels, markdown, tables) |
