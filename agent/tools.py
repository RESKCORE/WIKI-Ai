from langchain_core.tools import tool

from mcp_client.client import WikipediaMCPClient

client = WikipediaMCPClient()


def _coerce(value) -> str:
    """Force any input type into a clean string."""
    if isinstance(value, list):
        value = value[0] if value else ""
    elif isinstance(value, dict):
        value = value.get("title") or value.get("query") or value.get("page") or str(value)
    elif isinstance(value, bool):
        value = str(value)
    elif value is None:
        value = ""
    return str(value).strip()


@tool
def wikipedia_search(query: str) -> str:
    """Search Wikipedia for articles matching a query. Accepts any input type."""
    try:
        return client.call_tool("search_wikipedia", {"query": _coerce(query)})
    except Exception as e:
        return f"Error searching Wikipedia: {e}"


@tool
def wikipedia_summary(title: str) -> str:
    """Get a summary of a Wikipedia article by title. Accepts any input type."""
    try:
        return client.call_tool("get_summary", {"title": _coerce(title)})
    except Exception as e:
        return f"Error fetching summary: {e}"


@tool
def wikipedia_article(title: str) -> str:
    """Get the full content of a Wikipedia article by title. Accepts any input type."""
    try:
        return client.call_tool("get_article", {"title": _coerce(title)})
    except Exception as e:
        return f"Error fetching article: {e}"
