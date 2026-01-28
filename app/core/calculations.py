import numpy as np
from app.core.config import settings


# Функции формул
def linear(x, k, b):
    """Линейная формула y = k*x + b"""
    return k * x + b


def quadratic(x, a, b, c):
    """Квадратичная формула y = a*x^2 + b*x + c"""
    return a * x ** 2 + b * x + c


def exponential(x, a, b):
    """Экспоненциальная формула y = a*exp(b*x)"""
    return a * np.exp(b * x)


def logarithmic(x, a, b):
    """Логарифмическая формула y = a*log(x) + b, защитим от x <= 0"""
    x_safe = np.where(x <= 0, 1e-6, x)
    return a * np.log(x_safe) + b


def sinusoidal(x, a, b, c):
    """Синусоидальная формула y = a*sin(b*x + c)"""
    return a * np.sin(b * x + c)


# Словарь формул
formulas = {
    "linear": linear,
    "quadratic": quadratic,
    "exponential": exponential,
    "logarithmic": logarithmic,
    "sinusoidal": sinusoidal
}

# Параметры по умолчанию
default_params = {
    "linear": [settings.default_linear_k, settings.default_linear_b],  # k, b
    "quadratic": [settings.default_quadratic_a, settings.default_quadratic_b, settings.default_quadratic_c],  # a, b, c
    "exponential": [settings.default_exponential_a, settings.default_exponential_b],  # a, b
    "logarithmic": [1.0, 0.0],  # a, b
    "sinusoidal": [1.0, 1.0, 0.0]  # a, b, c
}


# Вычисление формулы
def compute_formula(formula_name, x, params=None):
    """
    Вычисляет значения y по формуле.

    :param formula_name: str - имя формулы ('linear', 'quadratic', 'exponential', 'logarithmic', 'sinusoidal')
    :param x: list или np.array - значения X
    :param params: list - параметры формулы (если None — используются дефолтные)
    :return: tuple (x, y) - массивы X и Y
    """
    x = np.array(x, dtype=float)

    if formula_name not in formulas:
        raise ValueError(f"Неверная формула: {formula_name}")

    if params is None:
        params = default_params[formula_name]

    y = formulas[formula_name](*([x] + params))
    return x, y

# import torch
# import numpy as np
# from app.core.config import settings
#
#
# # Формулы
# def linear(x, k, b):
#     return k * x + b
#
#
# def quadratic(x, a, b, c):
#     return a * x ** 2 + b * x + c
#
#
# def exponential(x, a, b):
#     return a * torch.exp(b * x)
#
#
# formulas = {
#     "linear": linear,
#     "quadratic": quadratic,
#     "exponential": exponential
# }
#
#
# # Вычисление
# def compute_formula(formula_name, x, param1=None, param2=None, param3=None):
#     x_tensor = torch.tensor(x, dtype=torch.float32)
#
#     if formula_name == "linear":
#         k = param1 if param1 is not None else settings.default_linear_k
#         b = param2 if param2 is not None else settings.default_linear_b
#         y_tensor = formulas["linear"](x_tensor, k, b)
#     elif formula_name == "quadratic":
#         a = param1 if param1 is not None else settings.default_quadratic_a
#         b_val = param2 if param2 is not None else settings.default_quadratic_b
#         c = param3 if param3 is not None else settings.default_quadratic_c
#         y_tensor = formulas["quadratic"](x_tensor, a, b_val, c)
#     elif formula_name == "exponential":
#         a = param1 if param1 is not None else settings.default_exponential_a
#         b_val = param2 if param2 is not None else settings.default_exponential_b
#         y_tensor = formulas["exponential"](x_tensor, a, b_val)
#     else:
#         raise ValueError("Неверная формула")
#
#     return x_tensor.numpy(), y_tensor.numpy()
#
