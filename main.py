#botree1/main.py
from fastapi import FastAPI
from routes.submit_complaint import router as submit_router
from routes.officer_dashboard import router as officer_router
from routes.login import login_router

from database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(submit_router)
app.include_router(login_router)
app.include_router(officer_router)

