from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

# 设置模板目录
templates_dir = Path(__file__).parent.parent / "templates"
templates = Jinja2Templates(directory=templates_dir)

router = APIRouter(tags=["pages"])

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """首页 - 笔记列表页面"""
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    """登录页面"""
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    """注册页面"""
    return templates.TemplateResponse("register.html", {"request": request})

@router.get("/notes/new", response_class=HTMLResponse)
async def new_note(request: Request):
    """创建新笔记页面"""
    return templates.TemplateResponse("note_editor.html", {"request": request})

@router.get("/notes/edit", response_class=HTMLResponse)
async def edit_note(request: Request):
    """编辑笔记页面"""
    return templates.TemplateResponse("note_editor.html", {"request": request})

@router.get("/notes/{note_id}", response_class=HTMLResponse)
async def note_detail(request: Request, note_id: str):
    """笔记详情页面"""
    return templates.TemplateResponse("note_detail.html", {"request": request})

@router.get("/offline.html", response_class=HTMLResponse)
async def offline_page(request: Request):
    """离线页面"""
    return templates.TemplateResponse("offline.html", {"request": request}) 