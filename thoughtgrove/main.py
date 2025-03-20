from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from thoughtgrove.api.auth import router as auth_router
from thoughtgrove.api.users import router as users_router
from thoughtgrove.api.notes import router as notes_router
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

# 注册路由
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(notes_router)

@app.get("/")
async def root():
    return {"message": "Welcome to ThoughtGrove API"} 