# import dependencies
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
import httpx
from contextlib import asynccontextmanager
import json
from starlette.config import Config
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()
config = Config(".env")

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.requests_client = httpx.AsyncClient()
    yield
    await app.requests_client.aclose()

# create app instance
app = FastAPI(lifespan=lifespan)

# set location for templates
templates = Jinja2Templates(directory="app/view_templates")

# handle http get requests for the site root /
# return the index.html page
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/advice", response_class=HTMLResponse)
async def advice(request: Request):
    
    # Define a request_client instance
    requests_client = request.app.requests_client

    # Connect to the API URL and await the response
    response = await requests_client.get(config("ADVICE_URL"))

    # Send the json data from the response in the TemplateResponse data parameter 
    return templates.TemplateResponse("advice.html", {"request": request, "data": response.json() })

# NASA APOD API details from the .env file
NASA_API_KEY = os.getenv("NASA_API_KEY")
NASA_APOD_URL = os.getenv("NASA_APOD_URL")

@app.get("/apod", response_class=HTMLResponse)
async def apod(request: Request):
    async with httpx.AsyncClient() as client:
        response = await client.get(NASA_APOD_URL)
        apod_data = response.json()  # Convert the response to JSON

    # Pass the APOD data to the template
    return templates.TemplateResponse("apod.html", {"request": request, "apod": apod_data})

@app.get("/params", response_class=HTMLResponse)
async def params(request: Request, name : str | None = ""):
    return templates.TemplateResponse("params.html", {"request": request, "name": name})

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):

    # get current date and time
    serverTime: datetime = datetime.now().strftime("%d/%m/%y %H:%M:%S")

    # note passing of parameters to the page
    return templates.TemplateResponse("index.html", {"request": request, "serverTime": serverTime})

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)