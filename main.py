#botree1/main.py
from fastapi import FastAPI
from routes.submit_complaint import router as submit_router
from routes.officer_dashboard import router as officer_router
from routes.grievance_details import router as grievance_details_router
from routes.admin_dashboard import router as admin_router
from routes.officer_create import router as officer_create_router
from routes.login import login_router
#from routes.grievance_tracking import router as tracking_router
from routes.officer_profile import router as officer_profile_router
from routes.admin_officer_profile import router as admin_officer_profile_router
from routes.admin_officer_list import router as admin_officer_list_router


from database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(submit_router)
app.include_router(login_router)#login for officer
app.include_router(officer_router)#matched grievances for officer dashboard
app.include_router(grievance_details_router)#get particular grievance detaile through grivance_id
app.include_router(admin_router)#grievances for admin dashboard
app.include_router(officer_create_router)#admin create officer
app.include_router(officer_profile_router)#officer can view their details and can update few things him self
app.include_router(admin_officer_profile_router)#admin get officer through email and can update details
app.include_router(admin_officer_list_router)#get all the officers to display in admion dashboard