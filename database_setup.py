import mysql.connector
from mysql.connector import Error
from datetime import datetime

# ---------------------- DB CONFIG ----------------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
    "database": "grievance_system"
}


# ---------------------- CONNECTION ----------------------
def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


# ---------------------- INIT DATABASE ----------------------
def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # ---------------- CITIZEN TABLE ----------------
    cur.execute("""
                CREATE TABLE IF NOT EXISTS citizen
                (
                    citizen_id
                    INT
                    AUTO_INCREMENT
                    PRIMARY
                    KEY,
                    citizen_surrogate_id
                    VARCHAR
                (
                    50
                ) NOT NULL DEFAULT
                (
                    UUID
                (
                )),
                    name VARCHAR
                (
                    255
                ),
                    phone VARCHAR
                (
                    20
                ),
                    email VARCHAR
                (
                    255
                ),
                    gender VARCHAR
                (
                    20
                ),
                    district TEXT,
                    mandal TEXT,
                    village_ward TEXT,
                    city VARCHAR
                (
                    255
                ),
                    pin_code VARCHAR
                (
                    10
                ),
                    address VARCHAR
                (
                    50
                ),
                    state VARCHAR
                (
                    255
                ),
                    country VARCHAR
                (
                    255
                ),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

    # ---------------- GRIEVANCE TABLE ----------------
    cur.execute("""
                CREATE TABLE IF NOT EXISTS grievance
                (
                    grievance_id
                    INT
                    PRIMARY
                    KEY
                    AUTO_INCREMENT,
                    complain_id
                    VARCHAR
                (
                    50
                ) NOT NULL DEFAULT
                (
                    UUID
                (
                )),
                    citizen_id INT,

                    source_system VARCHAR
                (
                    100
                ),
                    language VARCHAR
                (
                    50
                ),
                    text_complaint LONGTEXT,

                    latitude DECIMAL
                (
                    10,
                    6
                ),
                    longitude DECIMAL
                (
                    10,
                    6
                ),

                    category VARCHAR
                (
                    255
                ),
                    sub_category VARCHAR
                (
                    255
                ),

                    priority VARCHAR
                (
                    50
                ),
                    sentiment VARCHAR
                (
                    50
                ),
                    FOREIGN KEY
                (
                    citizen_id
                ) REFERENCES citizen
                (
                    Citizen_id
                )
                    )
                """)

    # ---------------- MEDIA FILES TABLE ----------------
    cur.execute("""
                CREATE TABLE IF NOT EXISTS media_files
                (
                    media_id
                    INT
                    AUTO_INCREMENT
                    PRIMARY
                    KEY,
                    grievance_id
                    INT,
                    file_type
                    ENUM
                (
                    'image',
                    'audio',
                    'video'
                ),
                    file_path TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY
                (
                    grievance_id
                ) REFERENCES grievance
                (
                    grievance_id
                )
                    )
                """)

    # ---------------- AI MODEL RESULTS ----------------
    cur.execute("""
                CREATE TABLE IF NOT EXISTS ai_results
                (
                    ai_id
                    INT
                    AUTO_INCREMENT
                    PRIMARY
                    KEY,
                    grievance_id
                    INT,

                    predicted_category
                    VARCHAR
                (
                    255
                ),
                    predicted_sub_category VARCHAR
                (
                    255
                ),
                    predicted_priority VARCHAR
                (
                    50
                ),

                    sentiment VARCHAR
                (
                    50
                ),
                    sentiment_score FLOAT,

                    accuracy FLOAT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY
                (
                    grievance_id
                ) REFERENCES grievance
                (
                    grievance_id
                )
                    )
                """)

    # ---------------- DEPARTMENT ----------------
    cur.execute("""
                CREATE TABLE IF NOT EXISTS department
                (
                    department_id
                    INT
                    AUTO_INCREMENT
                    PRIMARY
                    KEY,
                    department_name
                    VARCHAR
                (
                    255
                )
                    )
                """)

    # ---------------- OFFICER ----------------
    cur.execute("""
                CREATE TABLE IF NOT EXISTS officer
                (

                    officer_id
                    INT
                    AUTO_INCREMENT
                    PRIMARY
                    KEY,
                    name
                    VARCHAR
                (
                    100
                ),
                    department VARCHAR
                (
                    100
                ),
                    phone VARCHAR
                (
                    20
                ),
                    email VARCHAR
                (
                    50
                )
                    category_expertise VARCHAR
                (
                    100
                ),
                    city VARCHAR
                (
                    100
                ),
                    is_active BOOLEAN DEFAULT TRUE,
                    current_load INT DEFAULT 0
                    FOREIGN KEY
                (
                    department_id
                ) REFERENCES department
                (
                    department_id
                )
                    )
                """)

    # ---------------- GRIEVANCE PROCESSING TRACKER ----------------
    cur.execute("""
                CREATE TABLE IF NOT EXISTS grievance_tracking
                (
                    GPT_id
                    INT
                    AUTO_INCREMENT
                    PRIMARY
                    KEY,
                    grievance_id
                    INT,
                    officer_id
                    INT,
                    remarks
                    TEXT,

                    status
                    VARCHAR
                (
                    50
                ) DEFAULT 'Pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    resloved_at TIMESTAMP,

                    sla_days INT,
                    sla_breached BOOLEAN,
                    reopened_flag BOOLEAN,

                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY
                (
                    grievance_id
                ) REFERENCES grievance
                (
                    grievance_id
                ),
                    FOREIGN KEY
                (
                    officer_id
                ) REFERENCES officer
                (
                    officer_id
                )
                    )
                """)

    # ---------------- NOTIFICATIONS ----------------
    cur.execute("""
                CREATE TABLE IF NOT EXISTS notifications
                (
                    id
                    INT
                    AUTO_INCREMENT
                    PRIMARY
                    KEY,
                    type
                    VARCHAR
                (
                    100
                ),
                    message TEXT,
                    grievance_id INT,
                    time TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY
                (
                    grievance_id
                ) REFERENCES grievance
                (
                    grievance_id
                )
                    )
                """)

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Grievance System Database Initialized Successfully!")


# ---------------------- CITIZEN FUNCTIONS ----------------------
def insert_citizen(name, phone, email=None, gender=None, address=None, city=None, state=None, country=None):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
                INSERT INTO citizen (name, phone, email, gender, address, city, state, country)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (name, phone, email, gender, address, city, state, country))

    conn.commit()
    cid = cur.lastrowid
    cur.close()
    conn.close()
    return cid


# ---------------------- GRIEVANCE FUNCTIONS ----------------------
def insert_grievance(grievance_id, citizen_id, source_system, language, text, lat, lon,
                     category, sub_category, priority, sentiment):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
                INSERT INTO grievance
                (grievance_id, citizen_id, source_system, language, text_complaint,
                 latitude, longitude, category, sub_category, priority, sentiment)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (grievance_id, citizen_id, source_system, language, text,
                      lat, lon, category, sub_category, priority, sentiment))

    conn.commit()
    gid = cur.lastrowid
    cur.close()
    conn.close()
    return gid


def get_grievance_by_id(gid):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM grievance WHERE id=%s", (gid,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


# ---------------------- MEDIA FUNCTIONS ----------------------
def add_media(grievance_id, file_type, file_path):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
                INSERT INTO media_files (grievance_id, file_type, file_path)
                VALUES (%s, %s, %s)
                """, (grievance_id, file_type, file_path))

    conn.commit()
    cur.close()
    conn.close()
    return True


# ---------------------- OFFICER & TRACKING ----------------------
def assign_officer(grievance_id, officer_id, status="Assigned", remarks=None):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
                INSERT INTO grievance_tracking (grievance_id, officer_id, status, remarks)
                VALUES (%s, %s, %s, %s)
                """, (grievance_id, officer_id, status, remarks))

    conn.commit()
    cur.close()
    conn.close()
    return True


# ---------------------- NOTIFICATIONS ----------------------
def add_notification(type_, message, grievance_id=None):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
                INSERT INTO notifications (type, message, related_grievance_id)
                VALUES (%s, %s, %s)
                """, (type_, message, grievance_id))

    conn.commit()
    cur.close()
    conn.close()


#####################333
"""ALTER TABLE grievance
    ADD officer_id INT NULL,
ADD FOREIGN KEY (officer_id) REFERENCES officer(officer_id);"""