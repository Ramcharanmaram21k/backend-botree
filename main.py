import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Route Imports
from routes.submit_complaint import router as submit_router
from routes.officer_dashboard import router as officer_router
from routes.grievance_details import router as grievance_details_router
from routes.admin_dashboard import router as admin_router
from routes.officer_create import router as officer_create_router
from routes.login import login_router
from routes.officer_profile import router as officer_profile_router
from routes.admin_officer_profile import router as admin_officer_profile_router
from routes.admin_officer_list import router as admin_officer_list_router

from database import Base, engine

app = FastAPI()

# --- VERCEL FIX: USE TMP FOLDER ---
UPLOAD_DIR = "/tmp/uploads"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

# Mount the temporary directory
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "https://admin-officer-botree.vercel.app",
    "https://bo-tree-citizens.vercel.app",

    "https://bo-tree-citizens-git-main-ramcharans-projects-90b10c9a.vercel.app",

    "https://bo-tree-citizens-ramcharans-projects-90b10c9a.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(submit_router)
app.include_router(login_router)
app.include_router(officer_router)
app.include_router(grievance_details_router)
app.include_router(admin_router)
app.include_router(officer_create_router)
app.include_router(officer_profile_router)
app.include_router(admin_officer_profile_router)
app.include_router(admin_officer_list_router)