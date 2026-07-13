from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from agent.tools import wikipedia_search, wikipedia_summary, wikipedia_article
from prompts.system_prompt import SYSTEM_PROMPT
from config import GOOGLE_API_KEY, MODEL_NAME

llm = ChatGoogleGenerativeAI(model=MODEL_NAME, google_api_key=GOOGLE_API_KEY, temperature=0.2)
memory = MemorySaver()
tools = [wikipedia_search, wikipedia_summary, wikipedia_article]

agent = create_react_agent(llm, tools, prompt=SYSTEM_PROMPT, checkpointer=memory)
