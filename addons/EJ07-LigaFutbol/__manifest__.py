# -*- coding: utf-8 -*-
{
    'name': "Gestionar liga de futbol",
    'summary': "Gestionar una liga de futbol :) (Version avanzada)",
    'description': """
    Gestor de Liga de futbol (Version avanzada)
    ==============
    """,
    'application': True,
    'author': "Sergi Garcia",
    'website': "http://apuntesfpinformatica.es",
    'category': 'Tools',
    'version': '0.1',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/liga_equipo.xml',
        'views/liga_equipo_clasificacion.xml',
        'report/liga_equipo_clasificacion_report.xml',
        'report/liga_partido_report.xml',
        'views/liga_partido.xml',
        'wizard/liga_equipo_wizard.xml',
        'wizard/liga_partido_wizard.xml'
    ],
}
