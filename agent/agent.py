from langgraph.prebuilt import create_react_agent

from agent.llm import llm
from agent.tools import wikipedia_search, wikipedia_summary, wikipedia_article
from agent.memory import memory
from prompts.system_prompt import SYSTEM_PROMPT

tools = [wikipedia_search, wikipedia_summary, wikipedia_article]

agent = create_react_agent(
    llm,
    tools,
    prompt=SYSTEM_PROMPT,
    checkpointer=memory,
)
