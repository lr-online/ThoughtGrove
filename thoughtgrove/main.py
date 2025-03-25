from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.responses import FileResponse

from thoughtgrove.api.auth import router as auth_router
from thoughtgrove.api.users import router as users_router
from thoughtgrove.api.notes import router as notes_router
from thoughtgrove.pages import router as pages_router
from thoughtgrove.core.config import get_settings
from thoughtgrove.db.mongodb import mongodb

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动事件
    await mongodb.connect()
    yield
    # 关闭事件
    await mongodb.close()

app = FastAPI(
    title="ThoughtGrove API",
    description="拙园 - 数字化的私人思想园林",
    version="0.1.0",
    lifespan=lifespan
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制允许的源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录
static_dir = Path(__file__).parent.parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# 添加Service Worker路由
@app.get("/sw.js")
async def service_worker():
    return FileResponse(static_dir / "sw.js", media_type="application/javascript")

# 注册API路由
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(notes_router)

# 注册页面路由（优先级低于API路由）
app.include_router(pages_router)

@app.get("/")
async def root():
    return {"message": "Welcome to ThoughtGrove API"} 