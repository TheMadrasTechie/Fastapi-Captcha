from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()
templates = Jinja2Templates(directory="templates")

RECAPTCHA_SECRET_KEY = "YOUR_SECRET_KEY"  # Replace with your secret key

@app.get("/", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/submit")
async def submit_form(request: Request, name: str = Form(...), g_recaptcha_response: str = Form(...)):
    # Verify reCAPTCHA
    payload = {
        'secret': RECAPTCHA_SECRET_KEY,
        'response': g_recaptcha_response
    }
    r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=payload)
    result = r.json()

    if result.get("success"):
        return {"status": "success", "message": f"CAPTCHA Verified. Hello, {name}!"}
    else:
        return {"status": "error", "message": "CAPTCHA verification failed."}
