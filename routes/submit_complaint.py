# botree1/routes/submit_complaint.py
from fastapi import APIRouter, Depends, UploadFile, File, Form, Request
from sqlalchemy.orm import Session
import os
from functions.officer_assignment import OfficerAssignment
from models.officer import Officer
from database import SessionLocal
from functions.predict_priority import Priority
from models.citizen import Citizen
from models.grievance import Grievance
from models.media_files import MediaFile   # <- you must create this model
from typing import List
from functions.predict_sentiment import Sentiment
from functions.predict_category import Category
from functions.translation import Translation
from functions.device_detector import DeviceDetector

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(prefix="/submit", tags=["Submit"])


# @router.post("/")
# async def submit_form(
#     request: Request,   # <--- Added here
#     name: str = Form(...),
#     phone: str = Form(...),
#     email: str = Form(...),
#     gender: str = Form(...),
#     address: str = Form(...),
#     city: str = Form(...),
#     state: str = Form(...),
#     country: str = Form(...),
#     text_complaint: str = Form(...),
#     files: List[UploadFile] = File([]),
#     db: Session = Depends(get_db)
# ):
from typing import Optional

@router.post("/")
async def submit_form(
    request: Request,
    name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    gender: str = Form(...),
    district: str = Form(...),          # Changed from address
    mandal: str = Form(...),            # Changed from state
    village_ward: str = Form(...),      # Changed from country
    city: str = Form(...),
    text_complaint: str = Form(...),
    files: Optional[List[UploadFile]] = File(None),  # ✅ Changed this line
    db: Session = Depends(get_db)
):

    UPLOAD_DIR = "uploads/grievances"
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # 🔥  AUTO DETECT DEVICE SOURCE
    user_agent = request.headers.get("user-agent", "")
    source_system = DeviceDetector.detect_device(user_agent)

    # ---------------------------------------------------------------
    # 1️⃣ TEXT ANALYSIS
    # ---------------------------------------------------------------
    analysis = await Translation.analyze_text(text_complaint)
    detected_language = analysis["detected_language"]
    translated_text = analysis["translated_text"]

    auto_category = Category.predict_category_from_text(translated_text)
    auto_sentiment = Sentiment.predict_sentiment(translated_text)

    # ---------------------------------------------------------------
    # 2️⃣ EVIDENCE FLAGS
    # ---------------------------------------------------------------
    has_image = False
    has_video = False
    has_audio = False

    # ---------------------------------------------------------------
    # 3️⃣ Save CITIZEN
    # ---------------------------------------------------------------
    citizen = Citizen(
        name=name,
        phone=phone,
        email=email,
        gender=gender,
        district=district,  # ✅ Changed
        mandal=mandal,  # ✅ Changed
        village_ward=village_ward,  # ✅ Changed
        city=city,
    )
    db.add(citizen)
    db.flush()

    # ---------------------------------------------------------------
    # 4️⃣ Save GRIEVANCE
    # ---------------------------------------------------------------
    grievance = Grievance(
        citizen_id=citizen.citizen_id,
        source_system=source_system,
        language=detected_language,
        text_complaint=text_complaint,
        category=auto_category,
        sub_category="",
        priority="",
        sentiment=auto_sentiment,
        district=district,  # ✅ Added
        mandal=mandal,  # ✅ Added
        village_ward=village_ward,  # ✅ Added
    )
    db.add(grievance)
    db.flush()

    # # ---------------------------------------------------------------
    # # 3️⃣ Save CITIZEN
    # # ---------------------------------------------------------------
    # citizen = Citizen(
    #     name=name,
    #     phone=phone,
    #     email=email,
    #     gender=gender,
    #     address=address,
    #     city=city,
    #     state=state,
    #     country=country,
    # )
    # db.add(citizen)
    # db.flush()
    #
    # # ---------------------------------------------------------------
    # # 4️⃣ Save GRIEVANCE
    # # ---------------------------------------------------------------
    # grievance = Grievance(
    #     citizen_id=citizen.citizen_id,
    #     source_system=source_system,   # AUTO-DETECTED HERE
    #     language=detected_language,
    #     text_complaint=text_complaint,
    #     category=auto_category,
    #     sub_category="",
    #     priority="",
    #     sentiment=auto_sentiment,
    # )
    # db.add(grievance)
    # db.flush()

    # ---------------------------------------------------------------
    # 5️⃣ Save MEDIA
    # ---------------------------------------------------------------
    # saved_files = []
    #
    # for file in files:
    #     ext = file.filename.split(".")[-1].lower()
    #
    #     if ext in ["jpg", "jpeg", "png"]:
    #         file_type = "image"
    #         has_image = True
    #     elif ext in ["mp3", "wav"]:
    #         file_type = "audio"
    #         has_audio = True
    #     else:
    #         file_type = "video"
    #         has_video = True
    #
    #     file_path = f"{UPLOAD_DIR}/{grievance.grievance_id}_{file.filename}"
    #
    #     with open(file_path, "wb") as f:
    #         f.write(await file.read())
    #
    #     media = MediaFile(
    #         grievance_id=grievance.grievance_id,
    #         file_type=file_type,
    #         file_path=file_path
    #     )
    #     db.add(media)
    #     saved_files.append(file_path)
    # ---------------------------------------------------------------
    # 5️⃣ Save MEDIA
    # ---------------------------------------------------------------
    saved_files = []

    # ✅ Handle None case
    if files:
        for file in files:
            ext = file.filename.split(".")[-1].lower()

            if ext in ["jpg", "jpeg", "png"]:
                file_type = "image"
                has_image = True
            elif ext in ["mp3", "wav"]:
                file_type = "audio"
                has_audio = True
            else:
                file_type = "video"
                has_video = True

            file_path = f"{UPLOAD_DIR}/{grievance.grievance_id}_{file.filename}"

            with open(file_path, "wb") as f:
                f.write(await file.read())

            media = MediaFile(
                grievance_id=grievance.grievance_id,
                file_type=file_type,
                file_path=file_path
            )
            db.add(media)
            saved_files.append(file_path)

    # ---------------------------------------------------------------
    # 6️⃣ PRIORITY SCORE
    # ---------------------------------------------------------------
    priority_score, priority_level = Priority.compute_priority_score(
        category=auto_category,
        sentiment=auto_sentiment,
        has_image=has_image,
        has_video=has_video,
        has_audio=has_audio,
        rec_loc=False,
        rec_dept=False
    )
    grievance.priority = priority_level

    # ---------------------------------------------------------------
    # 7️⃣ AUTO ASSIGN OFFICER
    # ---------------------------------------------------------------
    # officer = OfficerAssignment.assign_officer(db, auto_category, city)
    #
    # if officer:
    #     grievance.officer_id = officer.officer_id
    #     officer.current_load += 1
    # else:
    #     grievance.officer_id = None
    #
    # db.commit()
    # ---------------------------------------------------------------
    # 7️⃣ AUTO ASSIGN OFFICER
    # ---------------------------------------------------------------
    officer = OfficerAssignment.assign_officer(
        db=db,
        category=auto_category,
        district=district,  # ✅ Changed from city
        mandal=mandal,  # ✅ Added
        village_ward=village_ward  # ✅ Added
    )

    if officer:
        grievance.officer_id = officer.officer_id
        officer.current_load += 1
    else:
        grievance.officer_id = None

    # ---------------------------------------------------------------
    # 8️⃣ FINAL RESPONSE
    # ---------------------------------------------------------------
    return {
        "message": "Grievance submitted successfully",
        "citizen_id": citizen.citizen_id,
        "grievance_id": grievance.grievance_id,
        "source_system": source_system,
        "detected_language": detected_language,
        "translated_text": translated_text,
        "auto_category": auto_category,
        "auto_sentiment": auto_sentiment,
        "priority_score": priority_score,
        "priority_level": priority_level,
        "uploaded_files": saved_files,
        "assigned_officer": officer.name if officer else "No suitable officer found",
        "officer_department": officer.department if officer else None
    }
