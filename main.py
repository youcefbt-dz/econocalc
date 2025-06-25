from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from routers import macro, finance, operations

app = FastAPI()

# إعداد القوالب والملفات الثابتة
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# الصفحة الرئيسية
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ربط الأقسام
app.include_router(macro.router, prefix="/macro")
app.include_router(finance.router, prefix="/finance")
app.include_router(operations.router, prefix="/operations")
