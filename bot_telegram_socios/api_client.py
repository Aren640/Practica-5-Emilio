import json
from typing import Dict, Tuple

import requests


class ApiClient:
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.endpoint = f"{self.base_url}/gestion/apirest/socio"

    def _safe_json(self, response: requests.Response) -> Dict:
        try:
            return response.json()
        except ValueError:
            return {}

    def crear_socio(self, nombre: str, apellidos: str, num_socio: str) -> Tuple[bool, str, Dict]:
        payload = {
            "nombre": nombre,
            "apellidos": apellidos,
            "num_socio": int(num_socio),
        }
        try:
            r = requests.post(self.endpoint, json=payload, timeout=self.timeout)
        except requests.RequestException:
            return False, "Error de conexion con Odoo", {}

        if r.status_code == 200:
            return True, "Socio creado correctamente", self._safe_json(r)
        return False, f"Error API ({r.status_code})", self._safe_json(r)

    def modificar_socio(self, nombre: str, apellidos: str, num_socio: str) -> Tuple[bool, str, Dict]:
        payload = {
            "nombre": nombre,
            "apellidos": apellidos,
            "num_socio": int(num_socio),
        }
        try:
            r = requests.put(self.endpoint, json=payload, timeout=self.timeout)
        except requests.RequestException:
            return False, "Error de conexion con Odoo", {}

        if r.status_code == 200:
            return True, "Socio modificado correctamente", self._safe_json(r)
        if r.status_code == 404:
            return False, "Socio no encontrado", self._safe_json(r)
        return False, f"Error API ({r.status_code})", self._safe_json(r)

    def consultar_socio(self, num_socio: str) -> Tuple[bool, str, Dict]:
        params = {"data": json.dumps({"num_socio": int(num_socio)})}
        try:
            r = requests.get(self.endpoint, params=params, timeout=self.timeout)
        except requests.RequestException:
            return False, "Error de conexion con Odoo", {}

        data = self._safe_json(r)
        if r.status_code == 200:
            return True, "OK", data
        if r.status_code == 404:
            return False, "Socio no encontrado", data
        return False, f"Error API ({r.status_code})", data

    def borrar_socio(self, num_socio: str) -> Tuple[bool, str, Dict]:
        params = {"data": json.dumps({"num_socio": int(num_socio)})}
        try:
            r = requests.delete(self.endpoint, params=params, timeout=self.timeout)
        except requests.RequestException:
            return False, "Error de conexion con Odoo", {}

        if r.status_code == 200:
            return True, "Socio eliminado correctamente", self._safe_json(r)
        if r.status_code == 404:
            return False, "Socio no encontrado", self._safe_json(r)
        return False, f"Error API ({r.status_code})", self._safe_json(r)
