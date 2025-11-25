# FastAPI Bigger Application for Car Shop ERP

![coverage](https://img.shields.io/badge/coverage-93%25-darkgreen)

This REST API serves as an ERP system for a car shop.

## Requirements

Ensure you have the following installed:

-   [Python 3.6~3.8](https://www.python.org/downloads/) (Verify runtime.txt)
-   [Virtual Environments with Python 3.6+](https://docs.python.org/3/tutorial/venv.html)

---

## Setup Project

1.  **Create a virtual environment:**
    
    ```bash
    python3 -m venv env
    ```
    
2.  **Activate the virtual environment:**
    
    ```bash
    source env/bin/activate
    ```
    
3.  **Install app dependencies:**
    
    ```bash
    pip install -r requirements.txt
    ```
    

---

## Running the Application

1.  **Start the application:**
    
    ```bash
    uvicorn app.main:app --reload
    ```
    

### Note:

You can configure the database using an environment variable:

```bash
export DB_URL="postgresql://user-name:password@host-name/database-name"
```

## Accessing the Application Locally

-   The application will be available at: [http://127.0.0.1:8000](http://127.0.0.1:8000)
-   Swagger Documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
-   Redoc Documentation: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

If

---

---

## Development

To update dependencies in `requirements.txt`:

1.  Remove the version constraint for `dataclasses`.
2.  Run:
    
    ```bash
    pip freeze > requirements.txt
    ```
    

---

---