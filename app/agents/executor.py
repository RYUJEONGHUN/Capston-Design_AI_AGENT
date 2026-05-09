from langchain_classic.agents import AgentType, initialize_agent

from app.agents.memory import get_memory
from app.core.factory import llm
from app.tools.course_tool import incheon_course_tool
from app.tools.incheon_tool import incheon_tool


def get_agent_executor(session_id: str):
    memory = get_memory(session_id)

    tools = [
        incheon_tool,
        incheon_course_tool,
    ]

    return initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        memory=memory,
        handle_parsing_errors=True,
        return_intermediate_steps=True,
        agent_kwargs={
            "memory_key": "chat_history",
            "input_variables": ["input", "agent_scratchpad", "chat_history"],
        },
    )