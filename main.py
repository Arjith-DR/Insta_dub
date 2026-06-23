from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from user.routers import user_routers
from core.routers import core_routers
from admin.routers import admin_routers

app = FastAPI()

root_dir = Path(__file__).resolve().parent
frontend_dir = root_dir / 'frontend'

app.mount('/static', StaticFiles(directory=frontend_dir), name='static')

@app.get('/')
async def serve_frontend():
    return FileResponse(frontend_dir / 'index.html')

# Include user routers
for router in user_routers:
    app.include_router(router, prefix='/api')

# Include core routers
for router in core_routers:
    app.include_router(router, prefix='/api')

# Include admin routers
for router in admin_routers:
    app.include_router(router, prefix='/api')
