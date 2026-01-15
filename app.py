#!/usr/bin/env python3
"""
FastAPI后端服务 - 为Simple Agent提供Web接口
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn

from simple_agent import SimpleAgent

app = FastAPI(title="Simple Agent Chat")

# 全局Agent实例
agent = None

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.on_event("startup")
async def startup_event():
    """启动时初始化Agent"""
    global agent
    try:
        agent = SimpleAgent()
        print("Agent初始化成功")
    except ValueError as e:
        print(f"Agent初始化失败: {e}")
        print("请确保设置了环境变量 OPENAI_BASE_URL 和 OPENAI_API_KEY")

@app.get("/")
async def root():
    """返回聊天页面"""
    return FileResponse("static/index.html")

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """处理聊天请求"""
    global agent
    if agent is None:
        raise HTTPException(status_code=500, detail="Agent未初始化，请检查环境变量")
    
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="消息不能为空")
    
    response = agent.chat(request.message)
    return ChatResponse(response=response)

@app.post("/api/reset")
async def reset():
    """重置对话历史"""
    global agent
    if agent is None:
        raise HTTPException(status_code=500, detail="Agent未初始化")
    
    agent.reset()
    return {"status": "ok", "message": "对话已重置"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
