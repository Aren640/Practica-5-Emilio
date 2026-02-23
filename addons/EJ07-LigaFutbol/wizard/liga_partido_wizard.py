# -*- coding: utf-8 -*-
from odoo import models, fields


class LigaPartidoWizard(models.TransientModel):
    _name = 'liga.partido.wizard'

    equipo_casa = fields.Many2one('liga.equipo', string='Equipo local', required=True)
    equipo_fuera = fields.Many2one('liga.equipo', string='Equipo visitante', required=True)
    goles_casa = fields.Integer()
    goles_fuera = fields.Integer()
    jornada = fields.Integer()

    def add_liga_partido(self):
        ligaPartidoModel = self.env['liga.partido']
        for wiz in self:
            ligaPartidoModel.create({
                'equipo_casa': wiz.equipo_casa.id,
                'equipo_fuera': wiz.equipo_fuera.id,
                'goles_casa': wiz.goles_casa,
                'goles_fuera': wiz.goles_fuera,
                'jornada': wiz.jornada,
            })
