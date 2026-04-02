from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
import asyncio
import json
from datetime import datetime

app = FastAPI()

# In-memory agent state
agents = {}

@app.get("/dashboard")
async def dashboard():
    """Serve the real-time agent monitoring dashboard"""
    return FileResponse("dashboard.html")

@app.post("/agent/heartbeat")
async def agent_heartbeat(agent_id: str, task: str, status: str, progress: int):
    """Agent sends status update"""
    agents[agent_id] = {
        "task": task,
        "status": status,
        "progress": progress,
        "last_update": datetime.utcnow().isoformat()
    }
    return {"received": True}

async def generate_updates():
    """Stream agent status changes to frontend"""
    while True:
        yield f"data: {json.dumps(agents)}\n\n"
        await asyncio.sleep(1)

@app.get("/stream/agents")
async def stream_agents():
    """SSE endpoint for real-time agent status"""
    return StreamingResponse(
        generate_updates(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
    )
