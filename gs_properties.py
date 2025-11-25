

class GSProperties:

    category_keywords = {
        "Law & Order": ["theft", "robbery", "assault", "police", "fight", "threat"],

        "Fire/Safety": ["fire", "burn", "danger", "smoke", "blast"],

        "Water Supply Issue": ["water", "pipeline", "burst", "leak", "no water", "tap", "drainage"],

        "Medical Emergency": ["injury", "ambulance", "bleeding", "medical", "unconscious", "heart attack"],

        "Electricity Issue": ["electric", "power", "meter", "transformer", "no power", "short circuit"],

        "Road Issue": ["pothole", "road", "hole", "damaged", "accident", "broken road"],

        "Garbage Issue": ["garbage", "waste", "trash", "dustbin", "dirty", "bad smell"],

        "Drainage Issue": ["drain", "drainage", "sewage", "clogged", "overflow"],

        "General Complaint": []
    }

    category_base = {
        "Law & Order": 100,
        "Fire/Safety": 95,
        "Water Supply Issue": 90,
        "Medical Emergency": 90,
        "Electricity Issue": 85,
        "Road Issue": 60,
        "Garbage Issue": 50,
        "Drainage Issue": 50,
        "General Complaint": 30
    }

    sentiment_score = {
        "Very Negative": 20,
        "Negative": 10,
        "Neutral": 0,
        "Positive": -10
    }
