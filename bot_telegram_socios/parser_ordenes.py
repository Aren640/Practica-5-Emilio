import re
from typing import Dict, Tuple

SUPPORTED_COMMANDS = {"crear", "modificar", "consultar", "borrar"}


def _parse_params(params_text: str) -> Dict[str, str]:
    pattern = r"(\w+)\s*=\s*\"([^\"]*)\""
    matches = re.findall(pattern, params_text)
    return {key.lower(): value for key, value in matches}


def parse_orden(text: str) -> Tuple[str, Dict[str, str], str]:
    """
    Devuelve:
    - action: crear/modificar/consultar/borrar/unsupported/error
    - params: parametros extraidos
    - error: mensaje de error si aplica
    """
    if not text or not text.strip():
        return "unsupported", {}, "Orden no soportada"

    raw = text.strip()
    first_part = raw.split(",", 1)[0].strip().lower()

    if first_part not in SUPPORTED_COMMANDS:
        return "unsupported", {}, "Orden no soportada"

    params_text = ""
    if "," in raw:
        params_text = raw.split(",", 1)[1]

    params = _parse_params(params_text)

    required = {
        "crear": {"nombre", "apellidos", "num_socio"},
        "modificar": {"nombre", "apellidos", "num_socio"},
        "consultar": {"num_socio"},
        "borrar": {"num_socio"},
    }

    missing = required[first_part] - set(params.keys())
    if missing:
        faltan = ", ".join(sorted(missing))
        return "error", {}, f"Formato incorrecto. Faltan: {faltan}"

    if not params.get("num_socio", "").isdigit():
        return "error", {}, "Formato incorrecto. num_socio debe ser numerico"

    return first_part, params, ""
