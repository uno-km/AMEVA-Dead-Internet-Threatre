import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session as DbSession
import logging

from src.db.database import init_db, get_db
from src.db.models import Session, Post, Comment, BotState
from src.orchestration.runner import run_session, restart_session
from src.orchestration.state_manager import state_manager, SystemState

templates = Jinja2Templates(directory="src/ui/templates")
logger = logging.getLogger("API")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. DB 초기화
    init_db()
    logger.info("[System] Database initialized. Waiting in IDLE state.")
    
    yield
    
    logger.info("[System] Shutting down AMEVA-DeadInternetSociety...")

app = FastAPI(title="AMEVA-DeadInternetSociety", lifespan=lifespan)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    메인 게시판 UI 렌더링 (SPA)
    """
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

@app.get("/api/posts")
async def get_posts(db: DbSession = Depends(get_db)):
    posts = db.query(Post).order_by(Post.id.desc()).all()
    return [{"id": p.id, "title": p.title, "created_at": p.created_at.strftime("%Y-%m-%d %H:%M:%S")} for p in posts]

@app.get("/api/posts/{post_id}")
async def get_post_detail(post_id: int, db: DbSession = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return {"error": "Post not found"}
        
    session_status = "UNKNOWN"
    session_obj = db.query(Session).filter(Session.id == post.session_id).first()
    if session_obj:
        session_status = session_obj.status

    comments = db.query(Comment).filter(Comment.post_id == post.id).order_by(Comment.created_at.asc()).all()
    
    comments_data = []
    for c in comments:
        comments_data.append({
            "id": c.id,
            "parent_id": c.parent_id,
            "bot_name": c.bot_name,
            "content": c.content,
            "anger_score": c.anger_score,
            "mentioned_bot": c.mentioned_bot,
            "created_at": c.created_at.strftime("%H:%M:%S")
        })
        
    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "session_status": session_status,
        "created_at": post.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "comments": comments_data
    }

@app.get("/api/bots/state")
async def get_bot_states(db: DbSession = Depends(get_db)):
    import json
    from src.orchestration.runner import calculate_effective_anger
    
    bot_states_db = db.query(BotState).all()
    bot_states = []
    
    # Get latest active session for status
    latest_session = db.query(Session).order_by(Session.id.desc()).first()
    session_status = latest_session.status if latest_session else "UNKNOWN"
    
    for b in bot_states_db:
        try:
            anger_dict = json.loads(b.anger_targets) if b.anger_targets else {}
        except:
            anger_dict = {}
        eff = calculate_effective_anger(anger_dict)
        bot_states.append({
            "bot_name": b.bot_name,
            "persona": b.persona,
            "current_directive": b.current_directive,
            "anger_targets": anger_dict,
            "effective_anger": eff
        })
        
    return {"states": bot_states, "session_status": session_status}

@app.get("/api/lpde/state")
async def get_lpde_states(db: DbSession = Depends(get_db)):
    import json
    from src.db.models import CurrentAgentState
    
    lpde_states = db.query(CurrentAgentState).all()
    results = []
    for s in lpde_states:
        def safe_load(val):
            try:
                return json.loads(val) if val else []
            except:
                return []
                
        results.append({
            "session_id": s.session_id,
            "bot_name": s.bot_name,
            "affect": safe_load(s.affect_json),
            "opinion": safe_load(s.opinion_json),
            "power": safe_load(s.power_json),
            "updated_at": s.updated_at.strftime("%Y-%m-%d %H:%M:%S") if s.updated_at else None
        })
    return {"lpde_states": results}

@app.get("/api/system/status")
async def get_system_status():
    import subprocess
    try:
        result = await asyncio.to_thread(
            subprocess.run, 
            ["docker", "ps", "--format", "{{.Names}}"], 
            capture_output=True, 
            text=True
        )
        running = result.stdout.strip().split("\n")
        
        containers = ["ameva-llm-main", "ameva-llm-god", "ameva-llm-bot-1", "ameva-llm-bot-2", "ameva-llm-bot-3"]
        status = {}
        for c in containers:
            status[c] = "RUNNING" if c in running else "STOPPED"
            
        return {
            "global_state": state_manager.state.value,
            "checkpoint": state_manager.checkpoint.value,
            **status
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/control/new")
async def control_new():
    if state_manager.state != SystemState.IDLE:
        return {"error": "명령어 수행중입니다. 동작 못합니다."}
    state_manager.set_state(SystemState.RUNNING)
    asyncio.create_task(run_session())
    return {"message": "New session started"}

@app.post("/api/control/pause")
async def control_pause():
    if state_manager.state == SystemState.IDLE:
        return {"error": "실행 중인 세션이 없습니다."}
    if state_manager.state in [SystemState.PAUSING, SystemState.PAUSED]:
        return {"error": "이미 중단 중이거나 중단된 상태입니다."}
    state_manager.set_state(SystemState.PAUSING)
    return {"message": "Pausing session..."}

@app.post("/api/control/resume")
async def control_resume():
    if state_manager.state == SystemState.IDLE:
        return {"error": "진행 중인 세션이 없습니다. 경고: 새로 시작하거나 이어하기를 이용하세요."}
    if state_manager.state == SystemState.RUNNING:
        return {"error": "이미 실행 중입니다."}
    state_manager.set_state(SystemState.RUNNING)
    return {"message": "Session resumed"}

@app.post("/api/control/stop")
async def control_stop():
    if state_manager.state == SystemState.IDLE:
        return {"error": "실행 중인 세션이 없습니다."}
    state_manager.set_state(SystemState.STOPPING)
    return {"message": "Stopping session..."}

@app.post("/api/control/restart/{post_id}")
async def control_restart(post_id: int, db: DbSession = Depends(get_db)):
    if state_manager.state != SystemState.IDLE:
        return {"error": "명령어 수행중입니다. 동작 못합니다."}
        
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return {"error": f"글 번호 {post_id}번을 찾을 수 없습니다."}
        
    session_id = post.session_id
    state_manager.set_state(SystemState.RUNNING)
    asyncio.create_task(restart_session(session_id))
    return {"message": f"Restarting post {post_id} (Session {session_id})"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("run:app", host="0.0.0.0", port=8050, reload=True)
