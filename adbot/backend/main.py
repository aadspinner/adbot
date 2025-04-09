from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import oracledb
import os
from dotenv import load_dotenv
load_dotenv()

# Env setup
os.environ["TNS_ADMIN"] = os.path.expanduser("~/oracle_wallet")
oracledb.init_oracle_client(lib_dir=os.path.expanduser("~/oracle_client/instantclient_23_7"))

# DB Config
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_DSN = os.getenv("DB_DSN")

# FastAPI setup
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    with oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT ID, NAME, EMAIL, PHONE, SUBMITTED_AT FROM LEADS ORDER BY SUBMITTED_AT DESC")
            leads = cursor.fetchall()
    return templates.TemplateResponse("dashboard.html", {"request": request, "leads": leads})
