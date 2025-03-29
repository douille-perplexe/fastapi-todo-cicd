from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from contextlib import asynccontextmanager

from app.routes import router

# Database initialization
def init_db():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        completed BOOLEAN NOT NULL DEFAULT 0
    )
    ''')
    conn.commit()
    conn.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database at startup
    init_db()
    yield
    # Cleanup on shutdown (if necessary)
    pass

# Create the FastAPI application
app = FastAPI(
    title="Todo API",
    description="Simple Todo API with CI/CD",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routes
app.include_router(router, prefix="/api")

# Root endpoint to check if the API is running
@app.get("/")
async def root():
    return {"message": "Todo API is running"}
