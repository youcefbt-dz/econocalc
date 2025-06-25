from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
import json

from services.operations_services import build_initial_simplex_tableau, pivot_simplex_step

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/simplex", response_class=HTMLResponse)
def simplex_get(request: Request):
    return templates.TemplateResponse("operations/simplex.html", {"request": request})


@router.post("/simplex", response_class=HTMLResponse)
def simplex_post(
    request: Request,
    objective: str = Form(...),
    constraints: str = Form(...),
    signs: str = Form(...),
    rhs: str = Form(...),
    maximize: Optional[str] = Form("on"),
    tableau_json: Optional[str] = Form(None),
    objective_json: Optional[str] = Form(None),
    header_json: Optional[str] = Form(None),
    basic_vars_json: Optional[str] = Form(None),
    step: Optional[str] = Form("initial")
):
    try:
        if step == "initial":
            obj = list(map(float, objective.strip().split(",")))
            cons = [list(map(float, row.strip().split(","))) for row in constraints.strip().split("\n")]
            rhs_vals = list(map(float, rhs.strip().split(",")))
            signs_list = signs.strip().split(",")

            result = build_initial_simplex_tableau(obj, cons, rhs_vals, signs_list, maximize == "on")

            return templates.TemplateResponse("operations/simplex.html", {
                "request": request,
                "step": step,
                "result": result,
                "input": {
                    "objective": objective,
                    "constraints": constraints,
                    "rhs": rhs,
                    "signs": signs,
                    "maximize": maximize
                },
                "tableau_json": json.dumps(result["tableau"]),
                "objective_json": json.dumps(result["objective"]),
                "header_json": json.dumps(result["header"]),
                "basic_vars_json": json.dumps(result["basic_vars"]),
                "header": result["header"],
                "basic_vars": result["basic_vars"]
            })

        elif step == "next":
            tableau = json.loads(tableau_json)
            objective = json.loads(objective_json)
            header = json.loads(header_json)
            basic_vars = json.loads(basic_vars_json)

            result = pivot_simplex_step(tableau, objective, basic_vars, header)

            return templates.TemplateResponse("operations/simplex.html", {
                "request": request,
                "step": step,
                "result": result,
                "tableau_json": json.dumps(result["tableau"]),
                "objective_json": json.dumps(result["objective"]),
                "header_json": json.dumps(result["header"]),
                "basic_vars_json": json.dumps(result["basic_vars"]),
                "header": result["header"],
                "basic_vars": result["basic_vars"]
            })

    except Exception as e:
        return templates.TemplateResponse("operations/simplex.html", {
            "request": request,
            "error": str(e)
        })
