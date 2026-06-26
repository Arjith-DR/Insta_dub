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

from settings.mongodb import get_mongo_db

@app.get('/api/ping-mongo')
async def ping_mongo():
    try:
        db = get_mongo_db()
        await db.command('ping')
        return {"status": "success", "message": "Connected to MongoDB Atlas successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Include user routers
for router in user_routers:
    app.include_router(router, prefix='/api')

# Include core routers
for router in core_routers:
    app.include_router(router, prefix='/api')

# Include admin routers
for router in admin_routers:
    app.include_router(router, prefix='/api')

from user.crud.mongo_likes import record_post_like
import traceback
@app.get('/api/test-like')
async def test_like():
    try:
        return await record_post_like(1, 1, 1)
    except Exception as e:
        return {'error': str(e), 'trace': traceback.format_exc()}
