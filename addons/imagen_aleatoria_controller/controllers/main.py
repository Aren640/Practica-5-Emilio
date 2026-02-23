# -*- coding: utf-8 -*-
import io
import json
import random

from PIL import Image

from odoo import http


MAX_SIZE = 1024


class ImagenAleatoriaController(http.Controller):
    @http.route('/imagenaleatoria', auth='public', type='http', methods=['GET'])
    def imagen_aleatoria(self, **kw):
        """
        Ejemplo:
        /imagenaleatoria?ancho=200&alto=100
        """
        ancho_raw = kw.get('ancho')
        alto_raw = kw.get('alto')

        if not ancho_raw or not alto_raw:
            return http.Response(
                json.dumps({"error": "Debes indicar ancho y alto"}),
                status=400,
                mimetype='application/json',
            )

        try:
            ancho = int(ancho_raw)
            alto = int(alto_raw)
        except ValueError:
            return http.Response(
                json.dumps({"error": "ancho y alto deben ser enteros"}),
                status=400,
                mimetype='application/json',
            )

        if ancho <= 0 or alto <= 0:
            return http.Response(
                json.dumps({"error": "ancho y alto deben ser mayores que 0"}),
                status=400,
                mimetype='application/json',
            )

        if ancho > MAX_SIZE or alto > MAX_SIZE:
            return http.Response(
                json.dumps({"error": f"Tamano maximo permitido: {MAX_SIZE}x{MAX_SIZE}"}),
                status=400,
                mimetype='application/json',
            )

        # Genera una lista RGB aleatoria: un color por pixel.
        pixels = [
            (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )
            for _ in range(ancho * alto)
        ]

        image = Image.new('RGB', (ancho, alto))
        image.putdata(pixels)

        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        buffer.seek(0)

        return http.Response(
            buffer.getvalue(),
            status=200,
            headers=[('Content-Type', 'image/png')],
        )
