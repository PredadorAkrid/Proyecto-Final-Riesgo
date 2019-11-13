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

#from flask_security.utils import hash_password
import psycopg2
from database import db_session
from database import Base
from flask_migrate import Migrate
from database import connection as cur
from security import *
#Instalar bcrypt
import json

##Importar modelos de models
from models import RegistroAlumno as RegistroAlumno
from models import Alumno as Alumno
from models import RegistroTutor as RegistroTutor
from models import Tutor as Tutor
from models import Actividad as Actividad
from models import Grupo as Grupo
from models import GrupoAlumno as GrupoAlumno
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

@app.after_request
def add_header(response):
	response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
	return response

#Vista de bienvenida, primera que cargamos
@app.route("/", methods=['GET', 'POST'])
def Index():
	if request.method == 'GET':
		
		
		
		return render_template("index.html")
	elif request.method == 'POST':
		
		
		
		if 'login_button' in request.form:
			usuario = request.form['usuario'];
			password = request.form['contraseña']
			
			resultAlumnosAux = db_session.query(RegistroAlumno).filter(RegistroAlumno.usuario == usuario).first()
			resultTutoresAux = db_session.query(RegistroTutor).filter(RegistroTutor.usuario == usuario).first()
			passwordFinal = ""
			if(resultAlumnosAux != None):
				if(verify_password(resultAlumnosAux.contraseña, password)):
					passwordFinal = resultAlumnosAux.contraseña
					result_alumnos = db_session.query(RegistroAlumno).filter(RegistroAlumno.usuario == usuario).filter(RegistroAlumno.contraseña == passwordFinal).first()
					print("entra a caso alumnos")
					session['nombre'] = usuario
					session['password'] = passwordFinal
					return redirect(url_for('Home'))
				else:
					flash("Contraseña incorrecta")
					print("contraseña alumno incorrecta")
					return redirect(url_for('Index'))
			elif(resultTutoresAux != None):

				if(verify_password(resultTutoresAux.contraseña, password)):
					passwordFinal = resultTutoresAux.contraseña
					result_tutores = db_session.query(RegistroTutor).filter(RegistroTutor.usuario == usuario).filter(RegistroTutor.contraseña ==  passwordFinal).first()
					print("entra a caso tutores")
					session['nombre'] = usuario
					session['password'] = passwordFinal
					return redirect(url_for('HomeTutor'))
				else:
					flash("Contraseña incorrecta")
					print("contraseña tutor incorrecta")
					return redirect(url_for('Index'))
			elif(resultAlumnosAux == None and resultTutoresAux == None):
				flash("Datos incorrectos")
				print("vacios los dos querys")
				return redirect(url_for('Index'))

			'''
			Esto jala si lo descomentamos y quitamos el else de arriba
			result_alumnos = db_session.query(RegistroAlumno).filter(RegistroAlumno.usuario == usuario).filter(RegistroAlumno.contraseña == passwordFinal).first()
			result_tutores = db_session.query(RegistroTutor).filter(RegistroTutor.usuario == usuario).filter(RegistroTutor.contraseña ==  passwordFinal).first()
			if(result_alumnos == None and result_tutores == None):
				flash("No existe el usario")
				print("entra al caso que no debe")
				return redirect(url_for('Index'))
			elif(result_alumnos != None):
				print("entra a caso alumnos")
				session['nombre'] = usuario
				session['password'] = passwordFinal
				
				return redirect(url_for('Home'))
			elif(result_tutores != None):
				print("entra a caso tutores")
				session['nombre'] = usuario
				session['password'] = passwordFinal
				return redirect(url_for('HomeTutor'))
			else:
				print("entra al else index")
				return redirect('/')
			'''
		elif 'register_button' in request.form:
			return redirect(url_for('Register')) # do something else
'''
@app.route("/inicial", methods=['GET', 'POST'])
def Inicial():
	if request.method == 'GET':
		print("Aquí hay que validar si ya está asociado a un grupo")
		return render_template('inicial.html')
	elif request.method == 'POST':
		if 'salir_button' in request.form:
			return removeSession()
		else:
			print("falta implementar éste caso")
'''
#@app.route("/registro-grupo", methods=['GET', 'POST'])
#def Inicial():
#	if request.method == 'GET':
#		return abort(403)
#	elif request.method == 'POST':
#		if 
def getSession():
	if 'nombre' in session:
		return session['nombre']
	return 'No existe una sesión activa'		
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
		return redirect(url_for(Index))
			
		
		
@app.route('/user_register', methods=['POST'])
def RegisterUser():
	if request.method == 'GET':
		return abort(403)
	elif request.method == 'POST':		
		print("esta llegando a ésto linea 205")	
		data = request.get_data(parse_form_data=False,  as_text=True)
		parsedData = data.split(',')
		print(parsedData)
		name = parsedData[0]
		usuario = parsedData[1]
		clave = parsedData[2]
		grupo = parsedData[3]
		claveCifrada = hash_password(clave)
		
		try:
    		
			inscrito = db_session.query(Grupo).filter(Grupo.idgrupo == grupo).first()
			if(inscrito != None):
				print("entra a inscrito")
				
				nuevoRegistro = RegistroAlumno(usuario = usuario, contraseña = claveCifrada)
				
				db_session.add(nuevoRegistro)
				db_session.commit()
				idRegistro = db_session.query(RegistroAlumno).filter(RegistroAlumno.usuario == usuario).filter(RegistroAlumno.contraseña == claveCifrada ).first()
				print("Imprimimos el id del registro del alumno")
				print(idRegistro.idregistroalumno)
				idAl = idRegistro.idregistroalumno
				nuevoAlumno =  Alumno(idregistroalumno= idAl, nombre=name)
				
				db_session.add(nuevoAlumno)
				db_session.commit()
				idAlumno = db_session.query(Alumno).filter(Alumno.idregistroalumno == idAl).first()
				print("El id del alumno es " + str(idAlumno.idalumno))

				grupAlu = GrupoAlumno(idgrupo = grupo , idalumno = idAlumno.idalumno)
				db_session.add(grupAlu)
				db_session.commit()

				newAct = Actividad(idgrupo=grupo, idalumno= idAlumno.idalumno)
				db_session.add(newAct)
				db_session.commit()
				return redirect(url_for('Index'))

			else:
				print("Aquí hay que meter un flush")
				db_session.rollback()
				return redirect(url_for('Register'))

		except:	
				print("Ocurrió una excepción")
				db_session.rollback()
				raise
				return removeSession()

		
#Ruta para el home
@app.route('/home', methods=['GET', 'POST'])
def Home():
	
	if request.method == 'GET':
		try:
			nombreUsuario =  session['nombre']
			password = session['password']
			print("En el home la contraseña es : " +  password)
			result_alumnos = db_session.query(RegistroAlumno).filter(RegistroAlumno.usuario == nombreUsuario).filter(RegistroAlumno.contraseña ==  password).first()
			if(result_alumnos == None):
				print("entra a la línea 200")
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
		
@app.route('/home_tutor', methods=['GET', 'POST'])
def HomeTutor():
	if request.method == 'GET':
		try:
			nombreTutor =  session['nombre']
			password = session['password']
			print("Esta es la contraseña del tutor: " + password)
			result_tutores = db_session.query(RegistroTutor).filter(RegistroTutor.usuario == nombreTutor).filter(RegistroTutor.contraseña ==  password).first()
			if(result_tutores == None):
				print("entra a la línea 226")
				return removeSession()
			else:
				return render_template("home-profe.html")
		except:
			return removeSession()
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

@app.route('/home/complementarias', methods=['GET','POST'])
def Complementarias():
	if 'nombre' in session:
		if request.method == 'GET':
			if 'nombre' in session:
				return render_template("complementarias.html")
			else:
				return removeSession()
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
					return removeSession()
			else:
				print("Entra a la línea 311")
				return redirect(url_for('Complementarias'))
	else:
		return removeSession()	
	
@app.route('/home/obligatorias', methods=['GET','POST'])
def Obligatorias():
	if 'nombre' in session:
		if request.method == 'GET':
			if 'nombre' in session:
				return render_template("obligatorias.html")
			else:
				return removeSession()
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
					return removeSession()
			else:
				print("Entra a la línea 377")
				return redirect(url_for('Obligatorias'))
	else:
		print("Entra a línea 382")
		return removeSession()	
	
@app.route('/home/obligatorias/unidad1/lectura01', methods=['GET','POST'])
def ObligatoriaU1L1():
	if request.method == 'GET':
		if 'nombre' in session:
			return render_template("obligatorias/unidad1/lectura01.html")
		else:
			return removeSession()
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
				
				else:
					print("Entra a la línea 306")
					return removeSession()
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
			return removeSession()
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
				
				else:
					print("Entra a la línea 306")
					return removeSession()
				
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
			return removeSession()
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
				
				else:
					print("Entra a la línea 306")
					return removeSession()
				
			elif 'lecturaO1.1_button' in request.form:
				return redirect(url_for('ObligatoriaU1L1'))
			elif 'lecturaCO1.2_button' in request.form:
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
			return removeSession()
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
				
				else:
					print("Entra a la línea 306")
					return removeSession()
					
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
			return removeSession()
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
				
				else:
					print("Entra a la línea 306")
					return removeSession()
				
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
			return removeSession()
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
				
				else:
					print("Entra a la línea 306")
					return removeSession()
					
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
				nombre =  session['nombre']
				password = session['password']
				result_tutores = db_session.query(RegistroTutor).filter(RegistroTutor.usuario == nombre).filter(RegistroTutor.contraseña ==  password).first()
				result_alumnos = db_session.query(RegistroAlumno).filter(RegistroAlumno.usuario == nombre).filter(RegistroAlumno.contraseña ==  password).first()
				if(result_tutores != None):
#p = db_session.query(Alumno).join(RegistroAlumno).filter(Alumno.idregistroalumno == RegistroAlumno.idregistroalumno).filter(RegistroAlumno.usuario == nombre).filter(RegistroAlumno.contraseña ==  password).first()					
					tutor = db_session.query(Tutor).join(RegistroTutor).filter(Tutor.idregistrotutor == result_tutores.idregistrotutor).filter(RegistroTutor.usuario == nombre).filter(RegistroTutor.contraseña ==  password).first()
					grupoTutor = db_session.query(Grupo).join(Tutor).filter(Grupo.idtutor == tutor.idtutor).first()
					result = db_session.query(Actividad).join(Grupo).filter(Actividad.idgrupo == grupoTutor.idgrupo).all()#meter datos del query
					
					listRes = []
					for student in result:
						alumno = db_session.query(Alumno).join(Actividad).filter(Alumno.idalumno == student.idalumno).first()
						auxLista = []
						auxLista.append(alumno.nombre)
						auxLista.append(student.actividad_1)
						auxLista.append(student.actividad_2)
						auxLista.append(student.actividad_3)
						auxLista.append(student.actividad_4)
						auxLista.append(student.actividad_5)
						auxLista.append(student.actividad_6)
						listRes.append(auxLista)
					print(listRes)
					return render_template("calificaciones.html", listRes=listRes)
				elif(result_alumnos != None):
					
					alumno = db_session.query(Alumno).join(RegistroAlumno).filter(Alumno.idregistroalumno == result_alumnos.idregistroalumno).filter(RegistroAlumno.usuario == nombre).filter(RegistroAlumno.contraseña ==  password).first()
					result = db_session.query(Actividad).join(Alumno).filter(Actividad.idalumno == alumno.idalumno).first()#meter datos del query
					listRes = []
					auxLista = []
					auxLista.append(alumno.nombre)
					auxLista.append(result.actividad_1)
					auxLista.append(result.actividad_2)
					auxLista.append(result.actividad_3)
					auxLista.append(result.actividad_4)
					auxLista.append(result.actividad_5)
					auxLista.append(result.actividad_6)
					listRes.append(auxLista)
					return render_template("calificaciones.html", listRes=listRes)
				else:
					return removeSession()
				
			else:
				return removeSession()
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
					return removeSession()
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
				return removeSession()
			else:
				return render_template("grupo.html")
		except:
			return removeSession()
	if request.method == 'POST':
		if 'salir_button' in request.form:
			return removeSession()
		elif 'home_button' in request.form:
			return redirect(url_for('HomeTutor'))
		#elif 'generarcodigo_button' in request.form:
		#	return "Aquí debe generar el código"
		else:
			print("No debería entrar aquí por ningún motivo linea 455")
@app.route('/home/complementarias/lectura01', methods=['GET', 'POST'])
def Complementaria01():
	if request.method == 'GET':
		if 'nombre' in session:
			return render_template("complementarias/lectura01.html")
		else:
			return removeSession()
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
				
				else:
					print("Entra a la línea 306")
					return removeSession()
					
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
				return removeSession()
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
				return removeSession()
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
@app.route('/calif-lectura', methods=['GET', 'POST'])
def Califica():
	if request.method == 'GET':
		return abort(403)
	if request.method == 'POST':
		if 'nombre' in session:
			print("Entra a enviar datos")
			nombre =  session['nombre']
			password = session['password']
			result_tutores = db_session.query(RegistroTutor).filter(RegistroTutor.usuario == nombre).filter(RegistroTutor.contraseña ==  password).first()
			result_alumnos = db_session.query(RegistroAlumno).filter(RegistroAlumno.usuario == nombre).filter(RegistroAlumno.contraseña ==  password).first()

			if(result_tutores != None):
				print("Error de acceso 403")
				return redirect(url_for('Obligatorias'))
			elif(result_alumnos != None):
				p = db_session.query(Alumno).join(RegistroAlumno).filter(Alumno.idregistroalumno == RegistroAlumno.idregistroalumno).filter(RegistroAlumno.usuario == nombre).filter(RegistroAlumno.contraseña ==  password).first()
				d = db_session.query(GrupoAlumno).join(Alumno).filter(GrupoAlumno.idalumno == Alumno.idalumno).filter(Alumno.idalumno == p.idalumno ).first()
			
				print("Entro a la 841")
				
				data = request.get_data(parse_form_data=False,  as_text=True)
				parseAux01 = data[0:15]
				
				
				parseAuxCalif = parseAux01[13:15]
				
				calificacionFinal = int(parseAuxCalif)
				parseAux02 = data[16:26]
				
				
				parseLectNum = parseAux02[8:10]
				lectFinal = int(parseLectNum)
				

				parseAux03 = data[27:]
				parseAuxUnidad = parseAux03[7:9]
				unidadFinal = int(parseAuxUnidad)
				
				consultaRegistroActividad = db_session.query(Actividad).filter(Actividad.idalumno == d.idalumno).filter(Actividad.idgrupo == d.idgrupo).first()
				if(consultaRegistroActividad == None):
					print("aquí insertamos")
				
				elif(consultaRegistroActividad != None):
					print("aquí actualizamos")
					string_campo = "actividad_" + str(lectFinal)
					cal = calificacionFinal
					print(string_campo)
					print(cal)
					loc = db_session.query(Actividad).filter(Actividad.idalumno == d.idalumno).filter(Actividad.idgrupo == d.idgrupo).first()
					if(lectFinal == 1):
						loc.actividad_1 = cal
						db_session.commit()
						print("Éxito al guardar")
						return redirect(url_for('Obligatorias'))
					elif(lectFinal == 2):
						loc.actividad_2 = cal
						db_session.commit()
						print("Éxito al guardar")
						return redirect(url_for('Obligatorias'))
					elif(lectFinal == 3):
						loc.actividad_3 = cal
						db_session.commit()
						print("Éxito al guardar")
						return redirect(url_for('Obligatorias'))
					elif(lectFinal == 4):
						loc.actividad_4 = cal
						db_session.commit()
						print("Éxito al guardar")
						return redirect(url_for('Obligatorias'))
					elif(lectFinal == 5):
						loc.actividad_5 = cal
						db_session.commit()
						print("Éxito al guardar")
						return redirect(url_for('Obligatorias'))
					elif(lectFinal == 6):
						loc.actividad_6 = cal
						db_session.commit()
						print("Éxito al guardar")
						return redirect(url_for('Obligatorias'))
					else:
						print("Error al guardar")
						return redirect(url_for('Obligatorias'))
			else:
				print("Entra a línea 870")
				return removeSession()
		else:
			print("No entra a enviar datos")
			return removeSession()


if __name__ == '__main__':
	app.run(port = 3000, debug = True)
