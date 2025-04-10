import os
import oracledb
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from datetime import timezone, timedelta


load_dotenv()
IST = timezone(timedelta(hours=5, minutes=30))

# Oracle client setup
oracledb.init_oracle_client(lib_dir="/app/oracle_client/instantclient_23_7")

# DB Config
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_DSN = os.getenv("DB_DSN")

# FastAPI setup
app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    with oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT ID, NAME, EMAIL, PHONE, SUBMITTED_AT FROM LEADS ORDER BY SUBMITTED_AT DESC")
            leads = cursor.fetchall()
    return templates.TemplateResponse("dashboard.html", {"request": request, "leads": leads})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
