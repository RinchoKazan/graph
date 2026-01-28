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


# @router.post("/plot")
# async def create_plot(
#     request: Request,
#     formula: str = Form(...),
#     x_values: str = Form(...),
#     param1: float = Form(None),
#     param2: float = Form(None),
#     param3: float = Form(None)
# ):
#     try:
#         # Конвертируем X
#         x_list = [float(i.strip()) for i in x_values.split(",") if i.strip()]
#         # if len(x_list) == 1:
#         #     x_list = list(np.linspace(x_list[0]-5, x_list[0]+5, 50))
#         # else:
#         #     x_list = list(np.linspace(min(x_list), max(x_list), 100))
#
#         if len(x_list) == 1:
#             x_list = np.linspace(x_list[0] - 5, x_list[0] + 5, 100)
#         else:
#             x_min, x_max = min(x_list), max(x_list)
#             if formula == "quadratic":
#                 # расширяем диапазон на 20% для лучшей визуализации параболы
#                 delta = (x_max - x_min) * 0.2
#                 if delta == 0:  # если все X одинаковы
#                     delta = 5
#                 x_list = np.linspace(x_min - delta, x_max + delta, 200)
#             else:
#                 x_list = np.linspace(x_min, x_max, 100)
#
#
#         # Собираем параметры
#         params = []
#         if formula == "linear":
#             params = [param1 or settings.default_linear_k, param2 or settings.default_linear_b]
#             params_dict = {"k": params[0], "b": params[1]}
#         elif formula == "quadratic":
#             params = [param1 or settings.default_quadratic_a,
#                       param2 or settings.default_quadratic_b,
#                       param3 or settings.default_quadratic_c]
#             params_dict = {"a": params[0], "b": params[1], "c": params[2]}
#         elif formula == "exponential":
#             params = [param1 or settings.default_exponential_a, param2 or settings.default_exponential_b]
#             params_dict = {"a": params[0], "b": params[1]}
#         else:
#             raise ValueError("Неверная формула")
#
#         x, y = compute_formula(formula, x_list, params)
#         graph_html = plot_graph(x, y, title=f"{formula.capitalize()} график", params=params_dict)
#
#     except ValueError as e:
#         logging.error(f"Ошибка вычислений: {e}")
#         return templates.TemplateResponse(
#             "index.html",
#             {"request": request, "graph": None, "error": str(e), "settings": settings}
#         )
#     except Exception as e:
#         logging.error(f"Непредвиденная ошибка: {e}")
#         return templates.TemplateResponse(
#             "index.html",
#             {"request": request, "graph": None, "error": "Произошла ошибка при построении графика.", "settings": settings}
#         )
#
#     # return templates.TemplateResponse(
#     #     "index.html",
#     #     {"request": request, "graph": graph_html, "error": None, "settings": settings}
#     # )
#     return templates.TemplateResponse(
#         "index.html",
#         {
#             "request": request,
#             "graph": graph_html,
#             "error": None,
#             "settings": settings,
#             "param1_value": param1 if param1 is not None else None,
#             "param2_value": param2 if param2 is not None else None,
#             "param3_value": param3 if param3 is not None else None,
#             "selected_formula": formula,
#             "x_values_value": x_values
#         }
#     )





