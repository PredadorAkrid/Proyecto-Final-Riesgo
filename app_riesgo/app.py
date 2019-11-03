#!/usr/bin/python
 # -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import session
from flask import escape
from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore,  login_required, UserMixin, RoleMixin
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask_security.utils import hash_password
import psycopg2
from database import db_session
from database import Base
from flask_migrate import Migrate
from database import connection as cur
#Instalar bcrypt


##Importar modelos de models
from models import RegistroAlumno as RegistroAlumno
from models import Alumno as Alumno
from models import RegistroTutor as RegistroTutor
from models import Tutor as Tutor



#Configuración del app y de la base
app = Flask(__name__)
app.secret_key = "qwerty@%1423"


#Comentado

POSTGRES = {
    'user': 'postgres',
    'pw': '1234',
    'db': 'dummy_db',
    'host': 'localhost',
    'port': '5432',
}


app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES



app.config['SECURITY_PASSWORD_SALT'] = 'ri3sg0-t3cn0l0gic0'
db = SQLAlchemy(app)

db.init_app(app)

'''
#db.init_app(app)
roles_users = db.Table('roles_users',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('role_id', db.Integer, db.ForeignKey('role.id')))
class User(db.Model,UserMixin):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(255))
	password = db.Column(db.String(255))
	active = db.Column(db.Boolean)
	confirmed_at = db.Column(db.DateTime)
	roles = db.relationship(
		'Role', 
		 secondary=roles_users,
		 backref=db.backref('users', lazy='dynamic')
	)
class Role(db.Model, RoleMixin):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(40))
	description = db.Column(db.String(255))

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)	
####Termina parte de security de momento
'''
######Declaración de modelos

######
@app.after_request
def add_header(response):
	response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
	return response
#Vista de bienvenida, primera que cargamos
@app.route("/", methods=['GET', 'POST'])
def Index():
	if request.method == 'GET':
		#print("Index session values: " , session['key_name'])
		#ésto mata todas las sesiones alv
		#session.pop('nombre', None)
		#session.pop('contraseña', None)
		return render_template("index.html")
	elif request.method == 'POST':
		

		#for clave in db_session.query(ent.clave):
		#		print(clave)
		if 'login_button' in request.form:
			usuario = request.form['usuario'];
			password = request.form['contraseña']
			#print(usuario, "   ", password)
			#Aquí obtenemos todos los elementos de la tabla
			
			#arr = db_session.query(DummyTable).all()
			#for r in arr:
			#	print(r)
			#Consulta personalizada
			#sql = "select *  from dummy_table"
			#res = db_session.execute(sql)
			#result = cur.execute("select * from dummy_table where nombre=%s AND contra=%s;",(usuario, password))
			result_alumnos = db_session.query(RegistroAlumno).filter(RegistroAlumno.usuario == usuario).filter(RegistroAlumno.contraseña == password).first()
			result_tutores = db_session.query(RegistroTutor).filter(RegistroTutor.usuario == usuario).filter(RegistroTutor.contraseña ==  password).first()
			
			
			#if(len(result) == 0):
			#	return redirect(url_for('/'))
			#else:
			if(result_alumnos == None and result_tutores == None):
				flash("No existe el usario")
				print("entra al caso que no debe")
				return redirect(url_for('Index'))
			elif(result_alumnos != None):
				print("entra a caso alumnos")
				session['nombre'] = usuario
				session['password'] = password
				print(result_alumnos.usuario)
				print(result_alumnos.contraseña)
				return redirect(url_for('Home'))
			elif(result_tutores != None):
				print("entra a caso tutores")
				session['nombre'] = usuario
				session['password'] = password
				return redirect(url_for('HomeTutor'))
			else:
				print("entra al else index")
				return redirect('/')
			#result = db_session.query(DummyTable)
			
			#names = [print(row) for row in result]
			#names = []
			#for row in result:
			#	names = row
			#print(names)
			##########################################################################Revisar
			'''
			if(usuario == 'Alexis'):
			#if(names[1] != None and names[2] != None):
				return redirect(url_for('Home'))
			else:
				return redirect('/')
			'''
		elif 'register_button' in request.form:
			#return redirect('Register')
			return redirect(url_for('Register')) # do something else
#@app.route('/getsession')
def getSession():
	if 'nombre' in session:
		return session['nombre']
	return 'No existe una sesión activa'		
#@app.route('/removesession')
def removeSession():
	if 'nombre' in session:
		print("borra la sesión")
		session.pop('nombre')
		return redirect(url_for('Index'))
	return redirect(url_for('Index')) 

#Ruta para vista de registro
@app.route('/register', methods=['GET', 'POST'])
def Register():
	if request.method == 'GET':
		return render_template("registro.html")
	elif request.method == 'POST':
		if 'back-button' in request.form:
			return redirect(url_for('Index'))
		elif 'register_button' in request.form:
			
			usuario = request.form['usuario']
			password = request.form['contraseña']
			passwordConf = request.form['contraseña_conf']
		####¿Lo necesitamos?
		#user_datastore.create_user(
		#	username = request.form.get('usuario'),
		#	password = hashpassword(request.form.get('contraseña'))
		#)
		#db.session.commit()
			return redirect(url_for('index'))

#Ruta para el home
@app.route('/home', methods=['GET', 'POST'])
def Home():
	
	if request.method == 'GET':
		try:
			nombreUsuario =  session['nombre']
			password = session['password']
			result_alumnos = db_session.query(RegistroAlumno).filter(RegistroAlumno.usuario == nombreUsuario).filter(RegistroAlumno.contraseña ==  password).first()
			if(result_alumnos == None):
				print("entra a la línea 200")
				#return redirect(url_for('Index'))
				return removeSession()
			else:
				print("entra a la línea 207")
				return render_template("home.html")
		except:
			return removeSession()
	
	if request.method == 'POST':
		if 'salir_button' in request.form:
			print("entra")
			return removeSession()
		elif 'complementarias_button' in request.form:
			print("entra a complementarias")
			return redirect(url_for("Complementarias"));
		elif 'obligatorias_button' in request.form:
			print("entra a obligatorias")
			return redirect(url_for("Obligatorias"))
		elif 'calificaciones_button' in request.form:
			return redirect(url_for("Calificaciones"))
		else:
			print("No debería entrar aquí por ningun motivo, línea 222")
		#print("Sesión inválida")
		#redirect(url_for('/'))

		#nombre = session['nombre']
		#contra = session['password']
		#print(nombre +  "  asd  " + contra)
@app.route('/home_tutor', methods=['GET', 'POST'])
def HomeTutor():
	if request.method == 'GET':
		try:
			nombreTutor =  session['nombre']
			password = session['password']
			result_tutores = db_session.query(RegistroTutor).filter(RegistroTutor.usuario == nombreTutor).filter(RegistroTutor.contraseña ==  password).first()
			if(result_tutores == None):
				print("entra a la línea 226")
				return redirect(url_for('Index'))
			else:
				return render_template("home-profe.html")
		except:
			return redirect(url_for('Index'))
	if request.method == 'POST':
		if 'salir_button' in request.form:
			return removeSession()
		elif 'complementarias_button' in request.form:
			print("entra a complementarias")
			return redirect(url_for("Complementarias"));
		elif 'obligatorias_button' in request.form:
			print("entra a obligatorias")
			return redirect(url_for("Obligatorias"))
		elif 'grupo_button' in request.form:
			return redirect(url_for("AltaGrupo"))
		elif 'calificaciones_button' in request.form:
			return redirect(url_for('Calificaciones'))
		else:
			print("No debería entrar aquí por ningún motivo linea 257")

		#print("Sesión inválida")
		#redirect(url_for('/'))

		#nombre = session['nombre']
		#contra = session['password']
		#print(nombre +  "  asd  " + contra)



@app.route('/home/complementarias', methods=['GET','POST'])
def Complementarias():
	if 'nombre' in session:
		if request.method == 'GET':
			if 'nombre' in session:
				return render_template("complementarias.html")
			else:
				return redirect(url_for('Index'))
		if request.method == 'POST':
			if 'salir_button' in request.form:
				print("entra")
				return removeSession()
			elif 'lecturaC1_button' in request.form:
				return redirect(url_for('Complementaria01'))
			elif 'lecturaC2_button' in request.form:
				return redirect(url_for('Complementaria02'))
			elif 'lecturaC3_button' in request.form:
				return redirect(url_for('Complementaria03'))
			elif 'home_button' in request.form:
				try:
					nombre =  session['nombre']
					password = session['password']
					result_tutores = db_session.query(RegistroTutor).filter(RegistroTutor.usuario == nombre).filter(RegistroTutor.contraseña ==  password).first()
					result_alumnos = db_session.query(RegistroAlumno).filter(RegistroAlumno.usuario == nombre).filter(RegistroAlumno.contraseña ==  password).first()
					if(result_tutores == None and result_alumnos == None):
						print("entra a la línea 298")
						return removeSession()
					elif(result_alumnos != None and result_tutores == None):
						return redirect(url_for('Home'))
					elif(result_tutores != None and result_alumnos == None):
						return redirect(url_for('HomeTutor'))

					else:
						print("Entra a la línea 306")
						return removeSession()
				except:
					return redirect(url_for('Index'))
			else:
				print("Entra a la línea 311")
				return redirect(url_for('Complementarias'))
	else:
		return removeSession()	
	'''
	if request.method == 'GET':
		if 'nombre' in session:
				return render_template("complementarias.html")
		else:
			return redirect(url_for('Index'))
	if request.method == 'POST':
		if 'salir_button' in request.form:
			print("entra")
			return removeSession()
		elif 'lectura_01_button' in request.form:
			return redirect(url_for('Complementaria01'))
		elif 'lectura_02_button' in request.form:
			return redirect(url_for('Complementaria02'))
		elif 'lectura_03_button' in request.form:
			return redirect(url_for('Complementaria03'))
		else:
			return redirect(url_for('Complementarias'))
	'''
@app.route('/home/obligatorias', methods=['GET','POST'])
def Obligatorias():
	if 'nombre' in session:
		if request.method == 'GET':
			if 'nombre' in session:
				return render_template("obligatorias.html")
			else:
				return redirect(url_for('Index'))
		if request.method == 'POST':
			if 'salir_button' in request.form:
				print("entra")
				return removeSession()
			elif 'lecturaO1.1_btn' in request.form:
				return redirect(url_for('ObligatoriaU1L1'))
			elif 'lecturaCO1.2_btn' in request.form:
				return redirect(url_for('ObligatoriaU1L2'))
			elif 'lecturaCO1.3_btn' in request.form:
				return redirect(url_for('ObligatoriaU1L3'))
			elif 'lecturaO2.1_btn' in request.form:
				return redirect(url_for('ObligatoriaU2L1'))
			elif 'lecturaCO2.2_btn' in request.form:
				return redirect(url_for('ObligatoriaU2L2'))
			elif 'lecturaCO2.3_btn' in request.form:
				return redirect(url_for('ObligatoriaU2L3'))	
			elif 'home_button' in request.form:
				try:
					nombre =  session['nombre']
					password = session['password']
					result_tutores = db_session.query(RegistroTutor).filter(RegistroTutor.usuario == nombre).filter(RegistroTutor.contraseña ==  password).first()
					result_alumnos = db_session.query(RegistroAlumno).filter(RegistroAlumno.usuario == nombre).filter(RegistroAlumno.contraseña ==  password).first()
					if(result_tutores == None and result_alumnos == None):
						print("entra a la línea 312")
						return removeSession()
					elif(result_alumnos != None and result_tutores == None):
						return redirect(url_for('Home'))
					elif(result_tutores != None and result_alumnos == None):
						return redirect(url_for('HomeTutor'))

					else:
						print("Entra a la línea 319")
						return removeSession()
				except:
					return redirect(url_for('Index'))
			else:
				print("Entra a la línea 377")
				return redirect(url_for('Obligatorias'))
	else:
		return removeSession()	
	'''
	if request.method == 'GET':
		if 'nombre' in session:
				return render_template("obligatorias.html")
		else:
			return redirect(url_for('Index'))
	if request.method == 'POST':
		if 'salir_button' in request.form:
			print("entra")
			return removeSession()
		elif 'lectura_01_button' in request.form:
			return redirect(url_for('Complementaria01'))
		elif 'lectura_02_button' in request.form:
			return redirect(url_for('Complementaria02'))
		elif 'lectura_03_button' in request.form:
			return redirect(url_for('Complementaria03'))
		else:
			return redirect(url_for('Obligatorias'))
'''
@app.route('/home/obligatorias/unidad1/lectura01', methods=['GET','POST'])
def ObligatoriaU1L1():
	if request.method == 'GET':
		if 'nombre' in session:
			return render_template("obligatorias/unidad1/lectura01.html")
		else:
			return redirect(url_for('Index'))
	if request.method == 'POST':
		if 'nombre' in session:
			if 'salir_button' in request.form:
				print("entra")
				return removeSession()
			elif 'menuO_button' in request.form:
				#try:
				print("Entra a menu o button en lectura 01")
				nombre =  session['nombre']
				password = session['password']
				result_tutores = db_session.query(RegistroTutor).filter(RegistroTutor.usuario == nombre).filter(RegistroTutor.contraseña ==  password).first()
				result_alumnos = db_session.query(RegistroAlumno).filter(RegistroAlumno.usuario == nombre).filter(RegistroAlumno.contraseña ==  password).first()
				if(result_tutores == None and result_alumnos == None):
					print("entra a la línea 298")
					return removeSession()
				elif(result_alumnos != None or result_tutores != None):
					return redirect(url_for('Obligatorias'))
				#elif(result_tutores != None and result_alumnos == None):
				#	return redirect(url_for('HomeTutor'))
				else:
					print("Entra a la línea 306")
					return removeSession()
					#except:
				#	return redirect(url_for('Index'))
			elif 'lecturaO1.2_button' in request.form:
				return redirect(url_for('ObligatoriaU1L2'))
			elif 'lecturaCO1.3_button' in request.form:
				return redirect(url_for('ObligatoriaU1L3'))
			else:
				print("entra a linea 500")
				return redirect(url_for('ObligatoriaU1L1'))
		else:
			return removeSession()
@app.route('/home/obligatorias/unidad1/lectura02', methods=['GET','POST'])
def ObligatoriaU1L2():
	if request.method == 'GET':
		if 'nombre' in session:
			return render_template("obligatorias/unidad1/lectura02.html")
		else:
			return redirect(url_for('Index'))
	if request.method == 'POST':
		if 'nombre' in session:
			if 'salir_button' in request.form:
				print("entra")
				return removeSession()
			elif 'menuO_button' in request.form:
				#try:
				print("Entra a menu o button en lectura 01")
				nombre =  session['nombre']
				password = session['password']
				result_tutores = db_session.query(RegistroTutor).filter(RegistroTutor.usuario == nombre).filter(RegistroTutor.contraseña ==  password).first()
				result_alumnos = db_session.query(RegistroAlumno).filter(RegistroAlumno.usuario == nombre).filter(RegistroAlumno.contraseña ==  password).first()
				if(result_tutores == None and result_alumnos == None):
					print("entra a la línea 298")
					return removeSession()
				elif(result_alumnos != None or result_tutores != None):
					return redirect(url_for('Obligatorias'))
				#elif(result_tutores != None and result_alumnos == None):
				#	return redirect(url_for('HomeTutor'))
				else:
					print("Entra a la línea 306")
					return removeSession()
					#except:
				#	return redirect(url_for('Index'))
			elif 'lecturaO1.1_button' in request.form:
				return redirect(url_for('ObligatoriaU1L1'))
			elif 'lecturaCO1.3_button' in request.form:
				return redirect(url_for('ObligatoriaU1L3'))
			else:
				print("entra a linea 500")
				return redirect(url_for('ObligatoriaU1L2'))
		else:
			return removeSession()
@app.route('/home/obligatorias/unidad1/lectura03', methods=['GET','POST'])
def ObligatoriaU1L3():
	if request.method == 'GET':
		if 'nombre' in session:
			return render_template("obligatorias/unidad1/lectura03.html")
		else:
			return redirect(url_for('Index'))
	if request.method == 'POST':
		if 'nombre' in session:
			if 'salir_button' in request.form:
				print("entra")
				return removeSession()
			elif 'menuO_button' in request.form:
				#try:
				print("Entra a menu o button en lectura 01")
				nombre =  session['nombre']
				password = session['password']
				result_tutores = db_session.query(RegistroTutor).filter(RegistroTutor.usuario == nombre).filter(RegistroTutor.contraseña ==  password).first()
				result_alumnos = db_session.query(RegistroAlumno).filter(RegistroAlumno.usuario == nombre).filter(RegistroAlumno.contraseña ==  password).first()
				if(result_tutores == None and result_alumnos == None):
					print("entra a la línea 298")
					return removeSession()
				elif(result_alumnos != None or result_tutores != None):
					return redirect(url_for('Obligatorias'))
				#elif(result_tutores != None and result_alumnos == None):
				#	return redirect(url_for('HomeTutor'))
				else:
					print("Entra a la línea 306")
					return removeSession()
					#except:
				#	return redirect(url_for('Index'))
			elif 'lecturaO1.1_button' in request.form:
				return redirect(url_for('ObligatoriaU1L1'))
			elif 'lecturaCO1.2_btn' in request.form:
				return redirect(url_for('ObligatoriaU1L2'))
			else:
				print("entra a linea 500")
				return redirect(url_for('ObligatoriaU1L3'))
		else:
			return removeSession()
@app.route('/home/obligatorias/unidad2/lectura01', methods=['GET','POST'])
def ObligatoriaU2L1():
	if request.method == 'GET':
		if 'nombre' in session:
			return render_template("obligatorias/unidad2/lectura01.html")
		else:
			return redirect(url_for('Index'))
	if request.method == 'POST':
		if 'nombre' in session:
			if 'salir_button' in request.form:
				print("entra")
				return removeSession()
			elif 'menuO_button' in request.form:
				#try:
				print("Entra a menu o button en lectura 01")
				nombre =  session['nombre']
				password = session['password']
				result_tutores = db_session.query(RegistroTutor).filter(RegistroTutor.usuario == nombre).filter(RegistroTutor.contraseña ==  password).first()
				result_alumnos = db_session.query(RegistroAlumno).filter(RegistroAlumno.usuario == nombre).filter(RegistroAlumno.contraseña ==  password).first()
				if(result_tutores == None and result_alumnos == None):
					print("entra a la línea 298")
					return removeSession()
				elif(result_alumnos != None or result_tutores != None):
					return redirect(url_for('Obligatorias'))
				#elif(result_tutores != None and result_alumnos == None):
				#	return redirect(url_for('HomeTutor'))
				else:
					print("Entra a la línea 306")
					return removeSession()
					#except:
				#	return redirect(url_for('Index'))
			elif 'lecturaO2.2_btn' in request.form:
				return redirect(url_for('ObligatoriaU2L2'))
			elif 'lecturaO2.3_btn' in request.form:
				return redirect(url_for('ObligatoriaU2L3'))
			else:
				print("entra a linea 500")
				return redirect(url_for('ObligatoriaU2L1'))
		else:
			return removeSession()
@app.route('/home/obligatorias/unidad2/lectura02', methods=['GET','POST'])
def ObligatoriaU2L2():
	if request.method == 'GET':
		if 'nombre' in session:
			return render_template("obligatorias/unidad2/lectura02.html")
		else:
			return redirect(url_for('Index'))
	if request.method == 'POST':
		if 'nombre' in session:
			if 'salir_button' in request.form:
				print("entra")
				return removeSession()
			elif 'menuO_button' in request.form:
				#try:
				print("Entra a menu o button en lectura 02")
				nombre =  session['nombre']
				password = session['password']
				result_tutores = db_session.query(RegistroTutor).filter(RegistroTutor.usuario == nombre).filter(RegistroTutor.contraseña ==  password).first()
				result_alumnos = db_session.query(RegistroAlumno).filter(RegistroAlumno.usuario == nombre).filter(RegistroAlumno.contraseña ==  password).first()
				if(result_tutores == None and result_alumnos == None):
					print("entra a la línea 298")
					return removeSession()
				elif(result_alumnos != None or result_tutores != None):
					return redirect(url_for('Obligatorias'))
				#elif(result_tutores != None and result_alumnos == None):
				#	return redirect(url_for('HomeTutor'))
				else:
					print("Entra a la línea 306")
					return removeSession()
					#except:
				#	return redirect(url_for('Index'))
			elif 'lecturaO2.1_button' in request.form:
				return redirect(url_for('ObligatoriaU2L1'))
			elif 'lecturaO2.3_button' in request.form:
				return redirect(url_for('ObligatoriaU2L3'))
			else:
				print("entra a linea 500")
				return redirect(url_for('ObligatoriaU2L2'))
		else:
			return removeSession()
@app.route('/home/obligatorias/unidad2/lectura03', methods=['GET','POST'])
def ObligatoriaU2L3():
	if request.method == 'GET':
		if 'nombre' in session:
			return render_template("obligatorias/unidad2/lectura03.html")
		else:
			return redirect(url_for('Index'))
	if request.method == 'POST':
		if 'nombre' in session:
			if 'salir_button' in request.form:
				print("entra")
				return removeSession()
			elif 'menuO_button' in request.form:
				#try:
				print("Entra a menu o button en lectura 01")
				nombre =  session['nombre']
				password = session['password']
				result_tutores = db_session.query(RegistroTutor).filter(RegistroTutor.usuario == nombre).filter(RegistroTutor.contraseña ==  password).first()
				result_alumnos = db_session.query(RegistroAlumno).filter(RegistroAlumno.usuario == nombre).filter(RegistroAlumno.contraseña ==  password).first()
				if(result_tutores == None and result_alumnos == None):
					print("entra a la línea 298")
					return removeSession()
				elif(result_alumnos != None or result_tutores != None):
					return redirect(url_for('Obligatorias'))
				#elif(result_tutores != None and result_alumnos == None):
				#	return redirect(url_for('HomeTutor'))
				else:
					print("Entra a la línea 306")
					return removeSession()
					#except:
				#	return redirect(url_for('Index'))
			elif 'lecturaO2.1_button' in request.form:
				return redirect(url_for('ObligatoriaU2L1'))
			elif 'lecturaO2.2_button' in request.form:
				return redirect(url_for('ObligatoriaU2L2'))
			else:
				print("entra a linea 500")
				return redirect(url_for('ObligatoriaU2L1'))
		else:
			return removeSession()
@app.route('/home_tutor/calificaciones', methods=['GET','POST'])
def Calificaciones():
	if 'nombre' in session:
		if request.method == 'GET':
			if 'nombre' in session:
				return render_template("calificaciones.html")
			else:
				return redirect(url_for('Index'))
		if request.method == 'POST':
			if 'salir_button' in request.form:
				print("entra")
				return removeSession()
			elif 'home_button' in request.form:
				try:
					nombre =  session['nombre']
					password = session['password']
					result_tutores = db_session.query(RegistroTutor).filter(RegistroTutor.usuario == nombre).filter(RegistroTutor.contraseña ==  password).first()
					result_alumnos = db_session.query(RegistroAlumno).filter(RegistroAlumno.usuario == nombre).filter(RegistroAlumno.contraseña ==  password).first()
					if(result_tutores == None and result_alumnos == None):
						print("entra a la línea 298")
						return removeSession()
					elif(result_alumnos != None and result_tutores == None):
						return redirect(url_for('Home'))
					elif(result_tutores != None and result_alumnos == None):
						return redirect(url_for('HomeTutor'))

					else:
						print("Entra a la línea 306")
						return removeSession()
				except:
					return redirect(url_for('Index'))
			else:
				return redirect(url_for('Calificaciones'))
	else:
		return removeSession()
@app.route('/home_tutor/grupo', methods=['GET','POST'])
def AltaGrupo():
	if request.method == 'GET':
		try:
			nombreTutor =  session['nombre']
			password = session['password']
			result_tutores = db_session.query(RegistroTutor).filter(RegistroTutor.usuario == nombreTutor).filter(RegistroTutor.contraseña ==  password).first()
			if(result_tutores == None):
				print("entra a la línea 445")
				return redirect(url_for('Index'))
			else:
				return render_template("grupo-crear.html")
		except:
			return redirect(url_for('Index'))
	if request.method == 'POST':
		if 'salir_button' in request.form:
			return removeSession()
		elif 'home_button' in request.form:
			return redirect(url_for('HomeTutor'))
		elif 'generarcodigo_button' in request.form:
			return "Aquí debe generar el código"
		else:
			print("No debería entrar aquí por ningún motivo linea 455")
@app.route('/home/complementarias/lectura01', methods=['GET', 'POST'])
def Complementaria01():
	if request.method == 'GET':
		if 'nombre' in session:
			return render_template("complementarias/lectura01.html")
		else:
			return redirect(url_for('Index'))
	if request.method == 'POST':
		if 'nombre' in session:
			if 'salir_button' in request.form:
				print("entra")
				return removeSession()
			elif 'menuC_button' in request.form:
				#try:
				print("Entra a menu c button en lectura 01")
				nombre =  session['nombre']
				password = session['password']
				result_tutores = db_session.query(RegistroTutor).filter(RegistroTutor.usuario == nombre).filter(RegistroTutor.contraseña ==  password).first()
				result_alumnos = db_session.query(RegistroAlumno).filter(RegistroAlumno.usuario == nombre).filter(RegistroAlumno.contraseña ==  password).first()
				if(result_tutores == None and result_alumnos == None):
					print("entra a la línea 298")
					return removeSession()
				elif(result_alumnos != None or result_tutores != None):
					return redirect(url_for('Complementarias'))
				#elif(result_tutores != None and result_alumnos == None):
				#	return redirect(url_for('HomeTutor'))
				else:
					print("Entra a la línea 306")
					return removeSession()
					#except:
				#	return redirect(url_for('Index'))
			elif 'lecturaC2_button' in request.form:
				return redirect(url_for('Complementaria02'))
			elif 'lecturaC3_button' in request.form:
				return redirect(url_for('Complementaria03'))
			else:
				print("entra a linea 500")
				return redirect(url_for('Complementaria01'))
		else:
			return removeSession()
@app.route('/home/complementarias/lectura02', methods=['GET', 'POST'])
def Complementaria02():
	if 'nombre' in session:
		if request.method == 'GET':
			if 'nombre' in session:
				return render_template("complementarias/lectura02.html")
			else:
				return redirect(url_for('Index'))
		if request.method == 'POST':
			if 'salir_button' in request.form:
				print("entra")
				return removeSession()
			elif 'menuC_button' in request.form:
				#try:
				nombre =  session['nombre']
				password = session['password']
				result_tutores = db_session.query(RegistroTutor).filter(RegistroTutor.usuario == nombre).filter(RegistroTutor.contraseña ==  password).first()
				result_alumnos = db_session.query(RegistroAlumno).filter(RegistroAlumno.usuario == nombre).filter(RegistroAlumno.contraseña ==  password).first()
				if(result_tutores == None and result_alumnos == None):
					print("entra a la línea 298")
					return removeSession()
				elif(result_alumnos != None or result_tutores != None):
					return redirect(url_for('Complementarias'))
				#elif(result_tutores != None and result_alumnos == None):
				#	return redirect(url_for('HomeTutor'))
				else:
					print("Entra a la línea 306")
					return removeSession()
				#except:
					#return redirect(url_for('Index'))
			elif 'lecturaC1_button' in request.form:
				return redirect(url_for('Complementaria01'))
			elif 'lecturaC3_button' in request.form:
				return redirect(url_for('Complementaria03'))
			else:
				print("entra a linea 500")
				return redirect(url_for('Complementaria02'))
	else:
		print("Entra a la línea 538")
		return removeSession()
@app.route('/home/complementarias/lectura03', methods=['GET', 'POST'])
def Complementaria03():
	if 'nombre' in session:
		if request.method == 'GET':
			if 'nombre' in session:
				return render_template("complementarias/lectura03.html")
			else:
				return redirect(url_for('Index'))
		if request.method == 'POST':
			if 'salir_button' in request.form:
				print("entra")
				return removeSession()
			elif 'menuC_button' in request.form:
				#try:
				nombre =  session['nombre']
				password = session['password']
				result_tutores = db_session.query(RegistroTutor).filter(RegistroTutor.usuario == nombre).filter(RegistroTutor.contraseña ==  password).first()
				result_alumnos = db_session.query(RegistroAlumno).filter(RegistroAlumno.usuario == nombre).filter(RegistroAlumno.contraseña ==  password).first()
				if(result_tutores == None and result_alumnos == None):
					print("entra a la línea 298")
					return removeSession()
				elif(result_alumnos != None or result_tutores != None):
					return redirect(url_for('Complementarias'))
				#elif(result_tutores != None and result_alumnos == None):
				#	return redirect(url_for('HomeTutor'))
				else:
					print("Entra a la línea 306")
					return removeSession()
				#except:
					#return redirect(url_for('Index'))
			elif 'lecturaC1_button' in request.form:
				return redirect(url_for('Complementaria01'))
			elif 'lecturaC3_button' in request.form:
				return redirect(url_for('Complementaria03'))
			else:
				print("entra a linea 500")
				return redirect(url_for('Complementaria02'))
	else:
		print("Entra a la línea 538")
		return removeSession()

if __name__ == '__main__':
	app.run(port = 3000, debug = True)
