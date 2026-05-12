from langchain_classic.agents import AgentType, initialize_agent

from app.tools.tool_factory import build_session_tools
from app.core.factory import qwen_agent_llm



def get_qwen_agent_executor(session_id: str):

    return initialize_agent(
        tools = build_session_tools(session_id),
        llm=qwen_agent_llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
        return_intermediate_steps=True,
    )