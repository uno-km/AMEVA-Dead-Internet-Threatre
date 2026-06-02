import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session as DbSession
import logging

from src.db.database import init_db, get_db
from src.db.models import Session, Post, Comment, BotState
from src.orchestration.runner import start_orchestrator_loop

templates = Jinja2Templates(directory="src/ui/templates")
logger = logging.getLogger("API")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. DB 초기화
    init_db()
    logger.info("[System] Database initialized.")
    
    # 2. 백그라운드 루프(스레드/비동기 태스크) 가동
    asyncio.create_task(start_orchestrator_loop())
    logger.info("[System] Orchestrator loop started.")
    
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
            "anger_targets": anger_dict,
            "eff_anger": eff
        })
    return {
        "session_status": session_status,
        "bots": bot_states
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("run:app", host="0.0.0.0", port=8050, reload=True)
