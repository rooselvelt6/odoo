# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime, timedelta

class ingreso(models.Model):

	_name = 'ingreso.ingreso'

	_rec_name = "nombre_completo"
	
	_description = "Ingresos"

	_order = 'fecha_ingreso_uci desc, nombre_completo asc'

	usuario_id = fields.Many2one('res.users', string='Responsable de la admisión', default=lambda self: self.env.user)

	active = fields.Boolean(string='Active', default=True)

	color = fields.Integer('Color')

	foto  = fields.Binary(string="Imagen del paciente", help='Imagen del paciente admitido', attachment=True)

	historia = fields.Char(string="Número de historia clínica", translate=True, size=7)

	nombre_completo = fields.Char(string='Nombre completo', translate=True, help='Nombre completo del paciente', required=True)

	nacionalidad = fields.Selection([(0,"V"),(1,"E")], string="Nacionalidad", default=0)

	ci = fields.Char(string='Cédula de identidad', size=9, help='Cédula de identidad')
	
	fecha_nacimiento  = fields.Date(string='Fecha de nacimiento', help='Fecha de nacimiento', required=True)
	
	edad = fields.Char(string='Edad del paciente', calculate="_calcularEdad", store=True)
	
	sexo = fields.Selection([(0,"Femenino"),(1,"Masculino")], default=0, string="Sexo")
	
	color_piel = fields.Selection([(0,"Morena"),(1,"Blanca")], string="Color de piel", default=0)

	pais_id = fields.Many2one('res.country','Pais', required=True)

	estado = fields.Many2one('res.country.state',"Estado de residencia")

	ciudad = fields.Many2one("res.city", string="Ciudad de origen", help='Ciudad de origen', required=True)

	lugar_nacimiento = fields.Text(string="Lugar de nacimiento", translate=True, help='Lugar de nacimiento', default="Cumaná, estado Sucre.")

	direccion = fields.Text(string="Dirección de hábitación actual", translate=True, help='Dirección actual')

	familiar_ids = fields.Many2many(
	    'ingreso.familiar',
	    string='Familiares en sala de espera',
	)

	fecha_ingreso_hospital  = fields.Date(string='Fecha de ingreso al HUAPA', help='Fecha de ingreso al Hospital', required=True)
	
	fecha_ingreso_uci = fields.Date(string="Fecha de ingreso a UCI", help='Fecha de Ingreso a UCI', required=True)

	estadia_hospitalaria = fields.Integer(calculate="_calcularEstadiaH", store=True, string="Estadía Hospitalaría General")

	antecedentes = fields.Text(string="Antecedentes del paciente", help='Antecedentes del paciente', default="")

	resumen_ingreso  = fields.Html(string='Resumen general de ingreso', translate=True, help='Resumen de ingreso del paciente', sanitize=True)

	diagnostico_HUAPA = fields.Html(string="Diagnóstico de ingreso al HUAPA", translate=True, help='Diagnóstico de ingreso al HUAPA', sanitize=True)

	diagnostico_UCI = fields.Html(string="Diagnóstico de ingreso a UCI", translate=True, help='Diagnóstico de ingreso a UCI', required=True, sanitize=True)

	examen_fisico_HUAPA = fields.Many2one(
	    'ingreso.examenfisico',
	    string='Examen físico de ingreso al HUAPA',
	    ondelete="cascade",
	    help='Examen físico de ingreso al HUAPA',
	    index=False,
	)

	examen_fisico_UCI = field_name = fields.Many2one(
	    'ingreso.examenfisico',
	    string='Examen físico de ingreso a UCI',
	    ondelete="cascade",
	    help='Examen físico de ingreso a UCI',
	    index=False,
	)
	
	tipo_admision = fields.Selection([(0,"Electiva"), (1,"Urgente")], string="Tipo de admisión", default=0)

	migracion = fields.Selection([(0,"No"), (1,"Si")], string="Proviene de migración", default=0)

	ventilacion_mecanica = fields.Selection([(0,"No"), (1,"Si")], string="Ventilador Mecánico", default=0)
	
	procesos_invasivos = fields.Selection([(0,"No"), (1,"Si")], string="Procesos invasivos", default=0)
	
	# Restricciones
	_sql_constraints = [
	    ('historia_uniq', 'unique (historia)', ('El número de Historia ya se encuentra registrado !!!')),
	    ('nombre_completo_uniq', 'unique (nombre_completo)', ('El paciente ya se encuentra registrado !!!')),
	    ('ci_uniq', 'unique (ci)', ('Cédula de identidad ya se encuentra registrada en el sistema !!!')),
	]

	@api.constrains('historia')
	def check_historia(self):
		"""if not self.historia:
			raise exceptions.ValidationError(
				'El número de historia debe ser completado !!!'
			)"""
		if(self.historia):
			if((len(self.historia) < 6)):
				raise exceptions.ValidationError(
					'El número de historia debe poseer un mínimo de 6 digitos !!!'
				)
			if((len(self.historia) > 7)):
				raise exceptions.ValidationError(
					'El número de historia debe poseer un máximo de 7 digitos !!!'
				)
			if(not self.historia.isdigit()):
				raise exceptions.ValidationError(
					"El número de historia no es válida !!!"
				)

			if (self.historia.isspace()):
				raise exceptions.ValidationError(
					"No se puede registrar una historia vacia !!!"
				)
			if (self.historia.isalpha()):
				raise exceptions.ValidationError(
					"Por favor ingresar un número de historia correcto !!!"
				)

	@api.constrains('nombre_completo')
	def check_nombre(self):
		if not self.nombre_completo:
			raise exceptions.ValidationError(
				'El número de historia debe ser completado !!!'
			)

		if((len(self.nombre_completo) > 35)):
			raise exceptions.ValidationError(
				'El nombre no debe exceder los 35 carácteres !!!'
			)

	# Funciones 
	@api.onchange('fecha_ingreso_uci','fecha_ingreso_hospital')
	def _calcularEstadiaH(self):
		if(self.fecha_ingreso_hospital and self.fecha_ingreso_uci):
			HUAPA = fields.Date.from_string(self.fecha_ingreso_hospital)
			UCI = fields.Date.from_string(self.fecha_ingreso_uci)
			self.estadia_hospitalaria = int(abs(((HUAPA - UCI).days)))

	@api.onchange('fecha_nacimiento')
	def _calcularEdad(self):
		if self.fecha_nacimiento:
			# Error existe en el calculo de la edad
			fecha_nacimiento = fields.Date.from_string(self.fecha_nacimiento)
			fecha_actual = fields.Date.from_string(datetime.now().strftime("%Y-%m-%d"))
			total = int(abs(((fecha_nacimiento - fecha_actual).days) / 365))
			self.edad = total

	@api.onchange('nombre_completo')
	def _adaptarNombre(self):
		
		if self.nombre_completo:
		
			nombre_mayusculas = self.nombre_completo.upper()

			self.nombre_completo = nombre_mayusculas
	
	

