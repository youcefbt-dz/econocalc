from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
from services.macro_services import (
    calculate_va, calculate_pib, calculate_pnb, calculate_pnn,
    calculate_rn, calculate_rp, calculate_rnd,
    calculate_inflation
)

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def to_float(val):
    try:
        return float(val)
    except (TypeError, ValueError):
        return None

@router.get("/inflation", response_class=HTMLResponse)
def inflation_calc(request: Request, cpi_old: float = 0, cpi_new: float = 0):
    attempted = True
    result = calculate_inflation(cpi_new, cpi_old)
    return templates.TemplateResponse("macro/inflation.html", {
        "request": request,
        "result": result,
        "attempted": attempted
    })

@router.get("/national-income", response_class=HTMLResponse)
def national_income_all(
    request: Request,
    p: Optional[str] = None, ci: Optional[str] = None,
    tva: Optional[str] = None, sub: Optional[str] = None,
    rfr: Optional[str] = None, rfv: Optional[str] = None,
    am: Optional[str] = None, indirect: Optional[str] = None,
    pr: Optional[str] = None, id1: Optional[str] = None,
    tr: Optional[str] = None, id2: Optional[str] = None
):
    # تحويل النصوص إلى أرقام
    p, ci = to_float(p), to_float(ci)
    va = calculate_va(p, ci) if p is not None and ci is not None else None

    tva, sub = to_float(tva), to_float(sub)
    pib = calculate_pib(va, tva, sub) if va is not None and tva is not None and sub is not None else None

    rfr, rfv = to_float(rfr), to_float(rfv)
    pnb = calculate_pnb(pib, rfr, rfv) if pib is not None and rfr is not None and rfv is not None else None

    am = to_float(am)
    pnn = calculate_pnn(pnb, am) if pnb is not None and am is not None else None

    indirect = to_float(indirect)
    rn = calculate_rn(pnn, indirect) if pnn is not None and indirect is not None else None

    pr, id1, tr = to_float(pr), to_float(id1), to_float(tr)
    rp = calculate_rp(rn, pr, id1, tr) if rn is not None and pr is not None and id1 is not None and tr is not None else None

    id2 = to_float(id2)
    rnd = calculate_rnd(rp, id2) if rp is not None and id2 is not None else None

    return templates.TemplateResponse("macro/national_income.html", {
        "request": request,
        "va": va, "pib": pib, "pnb": pnb, "pnn": pnn,
        "rn": rn, "rp": rp, "rnd": rnd,
        "values": {
            "p": p, "ci": ci, "va": va,
            "tva": tva, "sub": sub,
            "pib": pib,
            "rfr": rfr, "rfv": rfv,
            "pnb": pnb,
            "am": am,
            "indirect": indirect,
            "rn": rn,
            "pr": pr, "id1": id1, "tr": tr,
            "rp": rp,
            "id2": id2,
            "rnd": rnd
        }
    })
