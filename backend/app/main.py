from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.responses import RedirectResponse
from .routes.chat import router as chat_router

app = FastAPI(title="HVAC Design Assistant API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://hvac-assistant.azurewebsites.net"], # Azure deployed frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (e.g., favicon, CSS, JS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include chat API routes under /api
app.include_router(chat_router, prefix="/api")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# @app.get("/")
# async def root():
#     # Serve favicon or landing icon at root
#     return FileResponse("app/static/favicon-1-32x32.ico")

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

@app.get("/health")
def health():
    return {"status":"ok"}