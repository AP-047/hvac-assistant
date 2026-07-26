import threading
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.responses import RedirectResponse
from .routes.chat import router as chat_router

app = FastAPI(title="HVAC Technical Assistant API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow Vercel and all frontends
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def prewarm_embedder():
    try:
        from .services.retrieval import get_embedder
        print("⏳ Background pre-warming embedder model...")
        get_embedder()
        print("✅ Embedder model ready for instant answers!")
    except Exception as e:
        print(f"Embedder pre-warm error: {e}")

@app.on_event("startup")
async def startup_event():
    threading.Thread(target=prewarm_embedder, daemon=True).start()

# Include chat API routes under /api
app.include_router(chat_router, prefix="/api")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")