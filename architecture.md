# WikiResearch AI — Architecture

## High-Level Architecture

```mermaid
graph TB
    subgraph Terminal["🖥️  Terminal"]
        User["👤 User"]
        UI["rich Dashboard"]
    end

    subgraph App["🐍 Python App — app.py"]
        Loop["Interactive Loop"]
        Config["Thread Config"]
    end

    subgraph Agent["🤖 Agent — langgraph"]
        Router["create_react_agent"]
        Memory["MemorySaver"]
        Prompt["System Prompt"]
    end

    subgraph LLM["🧠 Gemini LLM"]
        Think["Reasoning / Decision"]
        Decide{"Needs\nWikipedia?"}
    end

    subgraph Tools["🔧 LangChain Tools"]
        T1["wikipedia_search"]
        T2["wikipedia_summary"]
        T3["wikipedia_article"]
    end

    subgraph MCP["📡 MCP Client"]
        Client["WikipediaMCPClient"]
        Session["Persistent Session"]
        Thread["Background Thread"]
    end

    subgraph Server["⚙️ wikipedia-mcp.exe"]
        StdIO["stdio Transport"]
        Handler["Tool Handler"]
    end

    subgraph Wiki["🌐 Wikipedia API"]
        API["en.wikipedia.org/w/api.php"]
    end

    User -->|"question"| UI
    UI -->|"input"| Loop
    Loop -->|"invoke"| Router
    Memory -.->|"chat history"| Router
    Prompt -.->|"instructions"| Router
    Router -->|"messages"| Think
    Think -->|"decide"| Decide
    Decide -->|"search"| T1
    Decide -->|"summary"| T2
    Decide -->|"article"| T3
    T1 -->|"call_tool"| Client
    T2 -->|"call_tool"| Client
    T3 -->|"call_tool"| Client
    Client -->|"coroutine"| Session
    Session -->|"stdio"| StdIO
    StdIO -->|"JSON-RPC"| Handler
    Handler -->|"HTTP GET"| API
    API -->|"JSON"| Handler
    Handler -->|"response"| StdIO
    StdIO -->|"result"| Session
    Session -->|"result"| Client
    Client -->|"text"| T1
    Client -->|"text"| T2
    Client -->|"text"| T3
    T1 -->|"tool result"| Router
    T2 -->|"tool result"| Router
    T3 -->|"tool result"| Router
    Router -->|"final answer"| Loop
    Loop -->|"render"| UI
    UI -->|"markdown"| User
```

## Request Flow — Single Question

```mermaid
sequenceDiagram
    autonumber
    participant U as 👤 User
    participant T as 🖥️ Terminal
    participant A as 🐍 App
    participant R as 🤖 Agent
    participant L as 🧠 Gemini
    participant W as 🔧 Wiki Tool
    participant M as 📡 MCP Client
    participant S as ⚙️ MCP Server
    participant K as 🌐 Wikipedia

    U->>T: "Who is Nikola Tesla?"
    T->>A: input()
    A->>R: agent.invoke(messages)
    R->>L: send to Gemini
    L->>L: Think: "I need Wikipedia"
    L->>R: Tool call: wikipedia_search
    R->>W: invoke("search_wikipedia", query)
    W->>M: call_tool("search_wikipedia", ...)
    M->>S: JSON-RPC over stdio
    S->>K: GET /w/api.php?action=query&list=search
    K-->>S: JSON results
    S-->>M: JSON response
    M-->>W: extracted text
    W-->>R: tool result
    R->>L: Observation: search results
    L->>L: Think: "Get summary of top result"
    L->>R: Tool call: wikipedia_summary
    R->>W: invoke("get_summary", "Nikola Tesla")
    W->>M: call_tool("get_summary", ...)
    M->>S: JSON-RPC over stdio
    S->>K: GET /w/api.php?action=query&prop=extracts
    K-->>S: article extract
    S-->>M: JSON response
    M-->>W: extracted text
    W-->>R: tool result
    R->>L: Observation: article summary
    L->>L: Think: "I have enough info"
    L-->>R: Final answer text
    R-->>A: result["messages"][-1]
    A-->>T: render Markdown
    T-->>U: formatted response
```

## Agent Decision Loop (ReAct Pattern)

```mermaid
flowchart TD
    Start(["User Question"])
    Think["🧠 Gemini thinks"]
    Action{"Needs tool?"}
    Tool["Call Wikipedia Tool"]
    MCP["MCP Client → Server → API"]
    Observe["Get result"]
    Answer["📝 Final Answer"]
    End(["User sees response"])

    Start --> Think
    Think --> Action
    Action -->|"yes"| Tool
    Tool --> MCP
    MCP --> Observe
    Observe --> Think
    Action -->|"no"| Answer
    Answer --> End
```

## MCP Communication Layer

```mermaid
graph LR
    subgraph Process["Python Process"]
        Sync["Sync call_tool()"]
        Loop["Background Event Loop"]
        Session["MCP ClientSession"]
    end

    subgraph IPC["stdio Pipe"]
        StdIn["stdin"]
        StdOut["stdout"]
    end

    subgraph WikiMCP["wikipedia-mcp.exe"]
        Server["MCP Server"]
        WikiAPI["wikipedia-api lib"]
    end

    subgraph Internet["Internet"]
        EnWiki["en.wikipedia.org"]
    end

    Sync -->|"run_coroutine_threadsafe"| Loop
    Loop -->|"await"| Session
    Session -->|"write JSON-RPC"| StdIn
    StdIn -->|"process stdin"| Server
    Server -->|"read JSON-RPC"| StdOut
    StdOut -->|"process stdout"| Session
    Server -->|"HTTP GET"| WikiAPI
    WikiAPI -->|"fetch"| EnWiki
    EnWiki -->|"JSON"| WikiAPI
    WikiAPI -->|"parse"| Server
```

## File Structure

```
wiki-agent/
├── app.py                      # Terminal dashboard + interactive loop
├── config.py                   # API keys, model config
├── requirements.txt
├── architecture.md             # This file
│
├── agent/
│   ├── __init__.py
│   ├── agent.py                # create_react_agent setup
│   ├── llm.py                  # Gemini LLM instance
│   ├── memory.py               # MemorySaver for conversation
│   └── tools.py                # LangChain tools wrapping MCP
│
├── mcp_client/
│   ├── __init__.py
│   └── client.py               # Persistent MCP client (1 subprocess)
│
├── prompts/
│   └── system_prompt.py        # WikiResearch AI instructions
│
└── utils/
    └── console.py
```
