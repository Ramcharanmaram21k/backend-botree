#botree1/main.py
from fastapi import FastAPI
from routes.submit_complaint import router as submit_router
from routes.officer_dashboard import router as officer_router
from routes.grievance_details import router as grievance_details_router
from routes.admin_dashboard import router as admin_router
from routes.officer_create import router as officer_create_router
from routes.login import login_router
#from routes.grievance_tracking import router as tracking_router

from database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(submit_router)
app.include_router(login_router)
app.include_router(officer_router)
app.include_router(grievance_details_router)
app.include_router(admin_router)
app.include_router(officer_create_router)