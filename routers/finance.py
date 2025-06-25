from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from services.finance_services import calculate_compound_interest  # تأكد أنها موجودة

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# ✅ عند زيارة /finance نعرض صفحة الأدوات
@router.get("/", response_class=HTMLResponse)
def finance_index(request: Request):
    return templates.TemplateResponse("finance/index.html", {"request": request})


# ✅ صفحة الفائدة المركبة
@router.get("/compound-interest", response_class=HTMLResponse)
def compound_interest(request: Request, principal: float = 0, rate: float = 0, time: float = 0, n: int = 1):
    result = calculate_compound_interest(principal, rate, time, n)
    return templates.TemplateResponse("finance/compound_interest.html", {
        "request": request,
        "result": result,
        "values": {
            "principal": principal,
            "rate": rate,
            "time": time,
            "n": n
        }
    })
from services.finance_services import calculate_simple_interest  # تأكد أنها موجودة

@router.get("/simple-interest", response_class=HTMLResponse)
def simple_interest(request: Request, principal: float = 0, rate: float = 0, time: float = 0):
    result = calculate_simple_interest(principal, rate, time)
    return templates.TemplateResponse("finance/simple_interest.html", {
        "request": request,
        "result": result,
        "values": {
            "principal": principal,
            "rate": rate,
            "time": time
        }
    })
