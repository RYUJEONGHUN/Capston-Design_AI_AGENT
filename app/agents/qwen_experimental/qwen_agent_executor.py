from langchain_classic.agents import AgentType, initialize_agent

from app.tools.course_tool import incheon_course_tool
from app.tools.qwen_experimental.incheon_tool_agent import incheon_tool_agent
from app.core.factory import qwen_agent_llm



def get_qwen_agent_executor():
    tools = [
        incheon_tool_agent,
        incheon_course_tool,
    ]

    return initialize_agent(
        tools=tools,
        llm=qwen_agent_llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
        return_intermediate_steps=True,
    )