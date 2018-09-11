# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Admision(models.Model):
	_name = "admision.admision"

	# FOTO DEL PACIENTE
	foto  = fields.Binary(string="Imagen del paciente", help='Imagen del paciente admitido')

	# ANTECEDENTES DE INGRESO
	antecedentes = fields.Html(translate=True, help='Antecedentes del paciente')
	
	# FECHA INGRESO A UCI
	fecha_ingreso_uci = fields.Date(string="Fecha de ingreso a UCI", help='Fecha de Ingreso a UCI')
	
	# DATOS DEL PACIENTE.
	datos_paciente = fields.Many2one('admision.paciente','Paciente')

	# RESUMEN DE INGRESO A UCI
	resumen_ingreso  = fields.Html(string='Resumen general de ingreso', translate=True, help='Resumen de ingreso del paciente')

	# EXAMEN FISICO DE INGRESO A UCI
	examen_fisico_uci = fields.Many2one('admision.examenfisico', 'Examen de ingreso a UCI')

	# DIAGNOSTICO DE INGRESO A UCI
	diagnostico_uci = fields.Many2one('admision.diagnostico', 'Diagnóstico de ingreso a UCI')
	
	# EVALUACION GENERAL DE INGRESO
	evaluacion_general = fields.Many2one('admision.evaluacion','Evaluación')
