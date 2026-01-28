from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from app.core.config import settings
from app.core.calculations import compute_formula, default_params
from app.core.plot_graph import plot_graph

import numpy as np
import logging
import os

router = APIRouter()
templates = Jinja2Templates(directory=os.path.join("app", "templates"))

logging.basicConfig(level=logging.INFO)

@router.get("/")
async def read_root(request: Request):
    # return templates.TemplateResponse(
    #     "index.html",
    #     {"request": request, "graph": None, "error": None, "settings": settings}
    # )

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "graph": None,
            "error": None,
            "settings": settings,
            "param1_value": None,
            "param2_value": None,
            "param3_value": None,
            "selected_formula": "linear",
            "x_values_value": "",
            "default_params": default_params
        }
    )

formula_params_map = {
    "linear": ["param1", "param2"],
    "quadratic": ["param1", "param2", "param3"],
    "exponential": ["param1", "param2"],
    "logarithmic": ["param1", "param2"],
    "sinusoidal": ["param1", "param2", "param3"]
}

@router.post("/plot")
async def create_plot(
    request: Request,
    formula: str = Form(...),
    x_values: str = Form(...),
    param1: float = Form(None),
    param2: float = Form(None),
    param3: float = Form(None)
):
    try:
        # Валидация X
        x_list = []
        for val in x_values.split(","):
            val = val.strip()
            if val == "":
                continue
            try:
                x_list.append(float(val))
            except ValueError:
                raise ValueError(f"Некорректное значение X: '{val}'")

        # Генерация диапазона X
        if len(x_list) == 1:
            x_list = np.linspace(x_list[0] - 5, x_list[0] + 5, 100)
        else:
            x_min, x_max = min(x_list), max(x_list)
            delta = (x_max - x_min) * 0.2 or 5
            x_list = np.linspace(x_min - delta, x_max + delta, 200)

        # Сбор параметров динамически
        param_values = [param1, param2, param3]
        keys = formula_params_map[formula]
        params = []
        params_dict = {}
        for i, key in enumerate(keys):
            value = param_values[i] if param_values[i] is not None else default_params[formula][i]
            params.append(value)
            params_dict[key[-1]] = value  # param1 -> "1", можно кастомно

        x, y = compute_formula(formula, x_list, params)
        graph_html = plot_graph(x, y, title=f"{formula.capitalize()} график", params=params_dict)

    except ValueError as e:
        return templates.TemplateResponse("index.html", {"request": request, "graph": None, "error": str(e), "settings": settings})

    except Exception as e:
        return templates.TemplateResponse("index.html", {"request": request, "graph": None, "error": "Произошла ошибка при построении графика.", "settings": settings})

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "graph": graph_html,
            "error": None,
            "settings": settings,
            "param1_value": param1,
            "param2_value": param2,
            "param3_value": param3,
            "selected_formula": formula,
            "x_values_value": x_values,
            "default_params": default_params
        }
    )
