from langchain_classic.agents import AgentType, initialize_agent

from app.core.factory import llm
from app.tools.tool_factory import build_session_tools
from app.core.persona import PERSONA_CONFIG
from app.agents.prompts import build_system_prompt


def get_agent_executor(
    session_id: str,
    persona_type: str,
    mbti_type: str | None = None,
    sasang_type: str | None = None,
):
    tools = build_session_tools(
        session_id,
        persona_type=persona_type,
        mbti_type=mbti_type,
        sasang_type=sasang_type,
    )
    print("[DEBUG][executor] tool classes =", [type(t).__name__ for t in tools])
    persona = PERSONA_CONFIG.get(persona_type, PERSONA_CONFIG["BEAR"])
    persona_info = persona["prompt"]

    system_prompt = build_system_prompt(
        persona_info=persona_info,
        mbti_type=mbti_type,
        sasang_type=sasang_type,
    )

    return initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        return_intermediate_steps=True,
        verbose=True,
        handle_parsing_errors=(
            "도구 호출 형식 오류입니다. JSON은 반드시 "
            "{\"action\": \"도구이름\", \"action_input\": \"사용자 질의\"} "
            "형식으로 다시 작성하세요. tool_input 키는 사용하지 마세요."
        ),
        agent_kwargs={
            "prefix": system_prompt,
            "suffix": (
                "이전 대화 기록:\n{chat_history}\n\n"
                "사용자 입력:\n{input}\n\n"
                "{agent_scratchpad}"
            ),
            "input_variables": ["input", "chat_history", "agent_scratchpad"],
        },
    )
