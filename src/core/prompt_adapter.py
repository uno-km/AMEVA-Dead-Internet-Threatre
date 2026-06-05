import logging
from typing import List
from src.db.models import Comment

logger = logging.getLogger("PromptAdapter")

class PromptAdapter:
    """
    LLM이 이전 대화를 '대본(Script)'으로 착각하고 다른 봇의 발화를 이어쓰는 
    할루시네이션(Hallucination)을 막기 위해, 대화 기록을 메타데이터 형태로 구조화합니다.
    """
    def __init__(self):
        pass

    def build_structured_history(self, items: List[dict]) -> str:
        """
        기존 "bot_1: 텍스트" 형식을 탈피하고 구조화된 로그 형태로 변환합니다.
        items는 {"bot_name": ..., "message": ...} 형태의 딕셔너리 리스트입니다.
        """
        if not items:
            return "No previous conversation."

        structured_lines = ["[Conversation History]"]
        for item in items:
            bot_name = item.get("bot_name", "Unknown")
            msg = item.get("message", "").strip()
            # 봇 이름이나 사람 이름을 명확히 분리하고, message를 데이터 필드로 취급
            line = f"- speaker={bot_name} | message=\"{msg}\""
            structured_lines.append(line)
        
        return "\n".join(structured_lines)

    def build_prompt(self, agent_state, history: str, target_bot: str) -> str:
        """
        Week 1B에서 적용될 전체 프롬프트 빌더. 
        (1A에서는 Shadow Mode이므로 사용하지 않음)
        """
        pass

prompt_adapter = PromptAdapter()
