import json
import math
import logging
from typing import Dict, List, Any
from sqlalchemy.orm import Session
from datetime import datetime

from src.db.models import CurrentAgentState, AgentStateSnapshot, EdgeState

logger = logging.getLogger("LPDE")

class PersonalityEngine:
    """
    Layered Personality Dynamics Engine (LPDE)
    Week 1A MVP: 
    - Shadow Mode (상태만 계산/저장하고 실제 프롬프트에 즉각적인 구조 개편은 유보)
    - 기저 성격(Traits)은 상수로, Affect(2D), Opinion(4D), Power(2D)만 업데이트
    """
    def __init__(self):
        # MVP용 기본 가중치 (추후 학습 또는 정교한 BFI-2 매핑으로 대체)
        self.clip_min = -1.0
        self.clip_max = 1.0

    def _clip(self, val: float) -> float:
        return max(self.clip_min, min(self.clip_max, val))

    def _sigmoid_bound(self, val: float) -> float:
        """비선형 활성화: 폭주를 막기 위해 tanh(val) 사용"""
        return math.tanh(val)

    def load_agent_state(self, db: Session, session_id: int, bot_name: str) -> CurrentAgentState:
        """기존 DB에서 로드, 없으면 새로 생성"""
        state = db.query(CurrentAgentState).filter(
            CurrentAgentState.session_id == session_id,
            CurrentAgentState.bot_name == bot_name
        ).first()
        if not state:
            state = CurrentAgentState(
                session_id=session_id,
                bot_name=bot_name,
                traits_json=json.dumps([0.0] * 22),
                states_json=json.dumps([0.0] * 10),
                affect_json=json.dumps([0.0, 0.0]), # [Valence, Arousal]
                memory_json=json.dumps([0.0] * 8), # [Issue commitment, etc]
                opinion_json=json.dumps([0.0, 0.0, 0.0, 0.0]), # [Stance, Gap, Moral]
                power_json=json.dumps([0.0, 0.0]), # [SelfAppraisal, SystemicInfluence]
                residual_json=json.dumps([0.0] * 16)
            )
            db.add(state)
            db.commit()
            db.refresh(state)
        return state

    def update_fast_state(self, db: Session, session_id: int, bot_name: str, turn_index: int):
        """
        턴이 끝날 때마다 호출되어 상태 공간을 업데이트합니다.
        (현재는 난수 또는 단순 decay 기반의 MVP 로직이며, Week 1B의 Event 추출기가 완성되면 Edge 기반 업데이트 추가)
        """
        agent = self.load_agent_state(db, session_id, bot_name)
        
        # Parse current states
        affect = json.loads(agent.affect_json)
        opinion = json.loads(agent.opinion_json)
        power = json.loads(agent.power_json)

        # [MVP Logic] 
        # 임시로 자연스러운 Decay (0으로 회귀) 및 소규모 변동성 부여
        # Affect: Arousal은 약간씩 가라앉고, Valence는 중립으로 회귀
        new_affect = [
            self._clip(self._sigmoid_bound(affect[0] * 0.9)), # Valence decay
            self._clip(self._sigmoid_bound(affect[1] * 0.95)) # Arousal decay
        ]

        # Opinion: 자신의 입장을 고수하려는 관성(Inertia)
        new_opinion = [self._clip(o * 0.98) for o in opinion]

        # Power: 서서히 변동
        new_power = [self._clip(p * 0.99) for p in power]

        # 상태 업데이트
        agent.affect_json = json.dumps(new_affect)
        agent.opinion_json = json.dumps(new_opinion)
        agent.power_json = json.dumps(new_power)
        db.commit()

        # 스냅샷 저장
        self.snapshot(db, session_id, turn_index, agent)

        logger.info(f"[LPDE] Updated Shadow State for {bot_name}: Affect={new_affect}")

    def snapshot(self, db: Session, session_id: int, turn_index: int, agent: CurrentAgentState):
        """턴이 종료될 때 스냅샷 테이블에 기록"""
        snap = AgentStateSnapshot(
            session_id=session_id,
            turn_index=turn_index,
            bot_name=agent.bot_name,
            traits_json=agent.traits_json,
            states_json=agent.states_json,
            affect_json=agent.affect_json,
            memory_json=agent.memory_json,
            opinion_json=agent.opinion_json,
            power_json=agent.power_json,
            residual_json=agent.residual_json
        )
        db.add(snap)
        db.commit()

personality_engine = PersonalityEngine()
