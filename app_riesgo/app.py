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
import psycopg2 #para la conexión a postgres
#Importamos la sesión para hacer consultas a la bd
from database import db_session
from database import Base
from flask_migrate import Migrate
from security import *
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
app.secret_key = "qwerty@%1423" #seed para las sesiones , encripta las sesiones



POSTGRES = {
    'user': 'postgres',
    'pw': '4l3xispassword#',
    'db': 'dummy_db',
    'host': 'localhost',
    'port': '5432',
}


app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES




#app.config['SECURITY_PASSWORD_SALT'] = 'ri3sg0-t3cn0l0gic0'
#Instanciamos el ORM
db = SQLAlchemy(app)

db.init_app(app)
"""
	Con ésto no permitimos el almacenamiento de caché, con lo cual no pueden retrocede a una página si ya no existe una sesión
"""
@app.after_request
def add_header(response):
	response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
	return response

"""
	Vista de bienvenida, primera que cargamos cuando el usuario abre localhost:3000
"""
@app.route("/", methods=['GET', 'POST'])
def Index():
	if request.method == 'GET':
		if 'nombre' in session:
			return removeSession()
		return render_template("index.html")
	elif request.method == 'POST':
		
		
		#Verificamos los datos que recibimos del form login
		if 'login_button' in request.form:
			usuario = request.form['usuario'];
			password = request.form['contraseña']
			#Hacemos unas consultas a la bd para ver si es un alumno o profesor
			resultAlumnosAux = db_session.query(RegistroAlumno).filter(RegistroAlumno.usuario == usuario).first()
			resultTutoresAux = db_session.query(RegistroTutor).filter(RegistroTutor.usuario == usuario).first()
			passwordFinal = ""
			if(resultAlumnosAux != None):
				#Si el if se cumple redireccionamos al home de alumno y creamos una sesión con su usuario/contraseña
				if(verify_password(resultAlumnosAux.contraseña, password)):
					passwordFinal = resultAlumnosAux.contraseña
					result_alumnos = db_session.query(RegistroAlumno).filter(RegistroAlumno.usuario == usuario).filter(RegistroAlumno.contraseña == passwordFinal).first()
					session['nombre'] = usuario
					session['password'] = passwordFinal
					return redirect(url_for('Home'))
				else:
					flash("Contraseña incorrecta")
					return redirect(url_for('Index'))
			elif(resultTutoresAux != None):
				#Si el if se cumple redireccionamos al home de profesor y creamos una sesión con su usuario/contraseña
				if(verify_password(resultTutoresAux.contraseña, password)):
					passwordFinal = resultTutoresAux.contraseña
					result_tutores = db_session.query(RegistroTutor).filter(RegistroTutor.usuario == usuario).filter(RegistroTutor.contraseña ==  passwordFinal).first()
					session['nombre'] = usuario
					session['password'] = passwordFinal
					return redirect(url_for('HomeTutor'))
				else:
					flash("Contraseña incorrecta")
					return redirect(url_for('Index'))
			elif(resultAlumnosAux == None and resultTutoresAux == None):
				flash("Datos incorrectos")
				return redirect(url_for('Index'))

			
		elif 'register_button' in request.form:
			return redirect(url_for('Register')) 
"""
	Método interno para remover una sesión si intentan redireccionar o pican el boton salir	
"""
def removeSession():
	if 'nombre' in session:
		session.pop('nombre')
		return redirect(url_for('Index'))
	return redirect(url_for('Index')) 
"""
	Ruta para vista de registro de alumnos
"""
@app.route('/register', methods=['GET', 'POST'])
def Register():
	if request.method == 'GET':
		if 'nombre' in session:
			return removeSession()
		return render_template("registro.html")
	elif request.method == 'POST':
		if 'back-button' in request.form:
			return redirect(url_for('Index'))
		return redirect(url_for(Index))
			
		
"""
	Ruta auxiliar para el registro de alumnos através de xmlhttprequest desde la vista
"""	
@app.route('/user_register', methods=['POST'])
def RegisterUser():
	#Si intentan hacer GET a ésta vista mandamos http 403
	if request.method == 'GET':
		return abort(403)
	elif request.method == 'POST':		
		data = request.get_data(parse_form_data=False,  as_text=True)
		parsedData = data.split(',')
		name = parsedData[0]
		usuario = parsedData[1]
		clave = parsedData[2]
		grupo = parsedData[3]
		claveCifrada = hash_password(clave)
		
		try:
    		
			inscrito = db_session.query(Grupo).filter(Grupo.idgrupo == grupo).first() #Checamos si existe el grupo que ingresó el usuario, si no le regresamos un mensaje de error
			if(inscrito != None):
				validaUsuario = db_session.query(RegistroAlumno).filter(RegistroAlumno.usuario == usuario).first()
				if(validaUsuario == None):
					nuevoRegistro = RegistroAlumno(usuario = usuario, contraseña = claveCifrada)
					db_session.add(nuevoRegistro)
					db_session.commit()
					idRegistro = db_session.query(RegistroAlumno).filter(RegistroAlumno.usuario == usuario).filter(RegistroAlumno.contraseña == claveCifrada ).first()
					idAl = idRegistro.idregistroalumno
					nuevoAlumno =  Alumno(idregistroalumno= idAl, nombre=name)
					db_session.add(nuevoAlumno)
					db_session.commit()
					idAlumno = db_session.query(Alumno).filter(Alumno.idregistroalumno == idAl).first()
					grupAlu = GrupoAlumno(idgrupo = grupo , idalumno = idAlumno.idalumno)
					db_session.add(grupAlu)
					db_session.commit()
					newAct = Actividad(idgrupo=grupo, idalumno= idAlumno.idalumno)
					db_session.add(newAct)
					db_session.commit()
					return redirect(request.path) #Si llega hasta aquí se registró con éxito el usuario
				else:
					#Si llega a éste punto entonces mandamos error al usuario de que ya existe el usuario que ingresó
					flash("El usuario ya existe")
					return redirect(request.path)
			else:
				flash("El grupo no existe")		#Si llega a éste punto entonces el grupo que introdujo no existe y le mandamos un mensaje
				
				return redirect(request.path)

		except:	
				db_session.rollback()
				raise
				return removeSession()

"""	
	Ruta para el home de alumno
"""
@app.route('/home', methods=['GET', 'POST'])
def Home():
	
	if request.method == 'GET':
		#Checa si existe una sesión válida al solicitar éste html, evitamos redireccionamiento
		try:
			nombreUsuario =  session['nombre']
			password = session['password']
			result_alumnos = db_session.query(RegistroAlumno).filter(RegistroAlumno.usuario == nombreUsuario).filter(RegistroAlumno.contraseña ==  password).first()
			if(result_alumnos == None):
				return removeSession()
			else:
				return render_template("home.html")
		except:
			return removeSession()
	#Aquí checamos todas las peticiones POST del usuario que activa al picar los botones
	if request.method == 'POST':
		if 'salir_button' in request.form:
			return removeSession()
		elif 'complementarias_button' in request.form:
			return redirect(url_for("Complementarias"));
		elif 'obligatorias_button' in request.form:
			return redirect(url_for("Obligatorias"))
		elif 'calificaciones_button' in request.form:
			return redirect(url_for("Calificaciones"))
		
"""
	Ruta para el home de un tutor con sesion válida
"""	
@app.route('/home_tutor', methods=['GET', 'POST'])
def HomeTutor():
	if request.method == 'GET':
		#Checa si existe una sesión activa para acceder al elemento, si la sesión no es de un tutor, elimina la sesión que mandó la petición
		try:
			nombreTutor =  session['nombre']
			password = session['password']
			result_tutores = db_session.query(RegistroTutor).filter(RegistroTutor.usuario == nombreTutor).filter(RegistroTutor.contraseña ==  password).first()
			if(result_tutores == None):
				return removeSession()
			else:
				return render_template("home-profe.html")
		except:
			return removeSession()
		#Checa las peticiones POST que manda el usuario através de los botones
	if request.method == 'POST':
		if 'salir_button' in request.form:
			return removeSession()
		elif 'complementarias_button' in request.form:
			return redirect(url_for("Complementarias"));
		elif 'obligatorias_button' in request.form:
			return redirect(url_for("Obligatorias"))
		elif 'grupo_button' in request.form:
			return redirect(url_for("AltaGrupo"))
		elif 'calificaciones_button' in request.form:
			return redirect(url_for('Calificaciones'))
		
"""
	Ruta para el menú principal de las lecturas complementarias
"""
@app.route('/home/complementarias', methods=['GET','POST'])
def Complementarias():
	#Checa si existe una sesión válida, ésta vista se comparte para mis dos tipos de usuarios
	if 'nombre' in session:
		if request.method == 'GET':
			#Checa si una sesión válida solicitó el recurso de lo contrario regresa al index 
			if 'nombre' in session:
				return render_template("complementarias.html")
			else:
				return removeSession()
		#Checa las peticiones POST que haga el usuario en ésta vista através de los botones
		if request.method == 'POST':
			if 'salir_button' in request.form:
				return removeSession()
			elif 'lecturaC1_button' in request.form:
				return redirect(url_for('Complementaria01'))
			elif 'lecturaC2_button' in request.form:
				return redirect(url_for('Complementaria02'))
			elif 'lecturaC3_button' in request.form:
				return redirect(url_for('Complementaria03'))
			elif 'home_button' in request.form:
				#Aquí como es una vista compartida, debemos ver si el propietario de la sesión es un alumno o un maestro
				#Entonces através de los datos de la sesión hacemos una consulta a la bdd y filtramos
				try:
					nombre =  session['nombre']
					password = session['password']
					result_tutores = db_session.query(RegistroTutor).filter(RegistroTutor.usuario == nombre).filter(RegistroTutor.contraseña ==  password).first()
					result_alumnos = db_session.query(RegistroAlumno).filter(RegistroAlumno.usuario == nombre).filter(RegistroAlumno.contraseña ==  password).first()
					if(result_tutores == None and result_alumnos == None):
						return removeSession()
					elif(result_alumnos != None and result_tutores == None):
						return redirect(url_for('Home'))
					elif(result_tutores != None and result_alumnos == None):
						return redirect(url_for('HomeTutor'))

					else:
						return removeSession()
				except:
					return removeSession()
			else:
				return redirect(url_for('Complementarias'))
	else:
		return removeSession()	
"""
	Ruta para el menú principal de las lecturas obligatorias
"""
@app.route('/home/obligatorias', methods=['GET','POST'])
def Obligatorias():
	#Si el if se cumple redireccionamos al home de alumno y creamos una sesión con su usuario/contraseña
	if 'nombre' in session:
		if request.method == 'GET':
			if 'nombre' in session:
				return render_template("obligatorias.html")
			else:
				return removeSession()
		#Aquí valida cuál es la lectura que requiere el usuario para redireccionarlo
		if request.method == 'POST':
			if 'salir_button' in request.form:
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
			#Al igual que otras vistas hay que checar si es alumno o profesor para ver qué vista mandarle
			elif 'home_button' in request.form:
				try:
					nombre =  session['nombre']
					password = session['password']
					result_tutores = db_session.query(RegistroTutor).filter(RegistroTutor.usuario == nombre).filter(RegistroTutor.contraseña ==  password).first()
					result_alumnos = db_session.query(RegistroAlumno).filter(RegistroAlumno.usuario == nombre).filter(RegistroAlumno.contraseña ==  password).first()
					if(result_tutores == None and result_alumnos == None):
						return removeSession()
					elif(result_alumnos != None and result_tutores == None):
						return redirect(url_for('Home'))
					elif(result_tutores != None and result_alumnos == None):
						return redirect(url_for('HomeTutor'))

					else:
						return removeSession()
				except:
					return removeSession()
			else:
				return redirect(url_for('Obligatorias'))
	else:
		return removeSession()	
"""
	Ruta para la lectura 1 unidad 1 
"""
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
				return removeSession()
			elif 'menuO_button' in request.form:
				#try:
				nombre =  session['nombre']
				password = session['password']
				result_tutores = db_session.query(RegistroTutor).filter(RegistroTutor.usuario == nombre).filter(RegistroTutor.contraseña ==  password).first()
				result_alumnos = db_session.query(RegistroAlumno).filter(RegistroAlumno.usuario == nombre).filter(RegistroAlumno.contraseña ==  password).first()
				if(result_tutores == None and result_alumnos == None):
					return removeSession()
				elif(result_alumnos != None or result_tutores != None):
					return redirect(url_for('Obligatorias'))
				
				else:
					return removeSession()
			elif 'lecturaO1.2_button' in request.form:
				return redirect(url_for('ObligatoriaU1L2'))
			elif 'lecturaCO1.3_button' in request.form:
				return redirect(url_for('ObligatoriaU1L3'))
			else:
				return redirect(url_for('ObligatoriaU1L1'))
		else:
			return removeSession()
"""
	Ruta para la lectura 2 unidad 1 
"""
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
				return removeSession()
			elif 'menuO_button' in request.form:
				nombre =  session['nombre']
				password = session['password']
				result_tutores = db_session.query(RegistroTutor).filter(RegistroTutor.usuario == nombre).filter(RegistroTutor.contraseña ==  password).first()
				result_alumnos = db_session.query(RegistroAlumno).filter(RegistroAlumno.usuario == nombre).filter(RegistroAlumno.contraseña ==  password).first()
				if(result_tutores == None and result_alumnos == None):
					return removeSession()
				elif(result_alumnos != None or result_tutores != None):
					return redirect(url_for('Obligatorias'))
				
				else:
					return removeSession()
				
			elif 'lecturaO1.1_button' in request.form:
				return redirect(url_for('ObligatoriaU1L1'))
			elif 'lecturaCO1.3_button' in request.form:
				return redirect(url_for('ObligatoriaU1L3'))
			else:
				return redirect(url_for('ObligatoriaU1L2'))
		else:
			return removeSession()
"""
	Ruta para la lectura 3 unidad 1 
"""
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
				return removeSession()
			elif 'menuO_button' in request.form:
				nombre =  session['nombre']
				password = session['password']
				result_tutores = db_session.query(RegistroTutor).filter(RegistroTutor.usuario == nombre).filter(RegistroTutor.contraseña ==  password).first()
				result_alumnos = db_session.query(RegistroAlumno).filter(RegistroAlumno.usuario == nombre).filter(RegistroAlumno.contraseña ==  password).first()
				if(result_tutores == None and result_alumnos == None):
					return removeSession()
				elif(result_alumnos != None or result_tutores != None):
					return redirect(url_for('Obligatorias'))
				
				else:
					return removeSession()
				
			elif 'lecturaO1.1_button' in request.form:
				return redirect(url_for('ObligatoriaU1L1'))
			elif 'lecturaCO1.2_button' in request.form:
				return redirect(url_for('ObligatoriaU1L2'))
			else:
				return redirect(url_for('ObligatoriaU1L3'))
		else:
			return removeSession()
"""
	Ruta para la lectura 1  unidad 2 
"""
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
				return removeSession()
			elif 'menuO_button' in request.form:
				#try:
				nombre =  session['nombre']
				password = session['password']
				result_tutores = db_session.query(RegistroTutor).filter(RegistroTutor.usuario == nombre).filter(RegistroTutor.contraseña ==  password).first()
				result_alumnos = db_session.query(RegistroAlumno).filter(RegistroAlumno.usuario == nombre).filter(RegistroAlumno.contraseña ==  password).first()
				if(result_tutores == None and result_alumnos == None):
					return removeSession()
				elif(result_alumnos != None or result_tutores != None):
					return redirect(url_for('Obligatorias'))
				
				else:
					return removeSession()
					
			elif 'lecturaO2.2_btn' in request.form:
				return redirect(url_for('ObligatoriaU2L2'))
			elif 'lecturaO2.3_btn' in request.form:
				return redirect(url_for('ObligatoriaU2L3'))
			else:
				return redirect(url_for('ObligatoriaU2L1'))
		else:
			return removeSession()
"""
	Ruta para la lectura 2 unidad 2
"""
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
				return removeSession()
			elif 'menuO_button' in request.form:
				
				nombre =  session['nombre']
				password = session['password']
				result_tutores = db_session.query(RegistroTutor).filter(RegistroTutor.usuario == nombre).filter(RegistroTutor.contraseña ==  password).first()
				result_alumnos = db_session.query(RegistroAlumno).filter(RegistroAlumno.usuario == nombre).filter(RegistroAlumno.contraseña ==  password).first()
				if(result_tutores == None and result_alumnos == None):
					return removeSession()
				elif(result_alumnos != None or result_tutores != None):
					return redirect(url_for('Obligatorias'))
				
				else:
					return removeSession()
				
			elif 'lecturaO2.1_button' in request.form:
				return redirect(url_for('ObligatoriaU2L1'))
			elif 'lecturaO2.3_button' in request.form:
				return redirect(url_for('ObligatoriaU2L3'))
			else:
				return redirect(url_for('ObligatoriaU2L2'))
		else:
			return removeSession()
"""
	Ruta para la lectura 2 unidad 3
"""
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
				return removeSession()
			elif 'menuO_button' in request.form:
				nombre =  session['nombre']
				password = session['password']
				result_tutores = db_session.query(RegistroTutor).filter(RegistroTutor.usuario == nombre).filter(RegistroTutor.contraseña ==  password).first()
				result_alumnos = db_session.query(RegistroAlumno).filter(RegistroAlumno.usuario == nombre).filter(RegistroAlumno.contraseña ==  password).first()
				if(result_tutores == None and result_alumnos == None):
					return removeSession()
				elif(result_alumnos != None or result_tutores != None):
					return redirect(url_for('Obligatorias'))
				
				else:
					return removeSession()
					
			elif 'lecturaO2.1_button' in request.form:
				return redirect(url_for('ObligatoriaU2L1'))
			elif 'lecturaO2.2_button' in request.form:
				return redirect(url_for('ObligatoriaU2L2'))
			else:
				return redirect(url_for('ObligatoriaU2L1'))
		else:
			return removeSession()
"""
	Método para obtener la calificación ya sea del alumno de forma individual o si es un maestro
	una tabla con las calificaciones de todos sus alumnos

"""
@app.route('/home_tutor/calificaciones', methods=['GET','POST'])
def Calificaciones():
	#Checamos si existe una sesión válida, si no borramos y mandamos al index
	if 'nombre' in session:
		
		if request.method == 'GET':
			if 'nombre' in session:
				nombre =  session['nombre']
				password = session['password']
				result_tutores = db_session.query(RegistroTutor).filter(RegistroTutor.usuario == nombre).filter(RegistroTutor.contraseña ==  password).first()
				result_alumnos = db_session.query(RegistroAlumno).filter(RegistroAlumno.usuario == nombre).filter(RegistroAlumno.contraseña ==  password).first()
				#Checamos si es un tutor si no pasamos a revisar si es un alumno
				if(result_tutores != None):
					tutor = db_session.query(Tutor).join(RegistroTutor).filter(Tutor.idregistrotutor == result_tutores.idregistrotutor).filter(RegistroTutor.usuario == nombre).filter(RegistroTutor.contraseña ==  password).first()
					grupoTutor = db_session.query(Grupo).join(Tutor).filter(Grupo.idtutor == tutor.idtutor).first()
					result = db_session.query(Actividad).join(Grupo).filter(Actividad.idgrupo == grupoTutor.idgrupo).all()#meter datos del query
					#Una vez obtenidos los datos del grupo de profesor pasamos a obtener los datos de los alumnos 
					listRes = []
					# guardamos en una lista de listas cada uno de los alumnos del grupo del profesor filtrando los atributos que
					# nos interesan del join
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
					return render_template("calificaciones.html", listRes=listRes) #mandamos al template de calificación los datos para la tabla
				#Checamos si es un alumno
				elif(result_alumnos != None):
					#repetimos un algoritmo similar al de tutor pero ahora solo nos interesa un registro (el del alumno)
					alumno = db_session.query(Alumno).join(RegistroAlumno).filter(Alumno.idregistroalumno == result_alumnos.idregistroalumno).filter(RegistroAlumno.usuario == nombre).filter(RegistroAlumno.contraseña ==  password).first()
					result = db_session.query(Actividad).join(Alumno).filter(Actividad.idalumno == alumno.idalumno).first()
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
					return render_template("calificaciones.html", listRes=listRes) #Regresamos el registro para la vista calificaciones
				else:
					return removeSession()
				
			else:
				return removeSession()
		#Manejamos las peticiones POST
		if request.method == 'POST':
			if 'salir_button' in request.form:
				return removeSession()
			elif 'home_button' in request.form:
				try:
					nombre =  session['nombre']
					password = session['password']
					result_tutores = db_session.query(RegistroTutor).filter(RegistroTutor.usuario == nombre).filter(RegistroTutor.contraseña ==  password).first()
					result_alumnos = db_session.query(RegistroAlumno).filter(RegistroAlumno.usuario == nombre).filter(RegistroAlumno.contraseña ==  password).first()
					if(result_tutores == None and result_alumnos == None):
						return removeSession()
					elif(result_alumnos != None and result_tutores == None):
						return redirect(url_for('Home'))
					elif(result_tutores != None and result_alumnos == None):
						return redirect(url_for('HomeTutor'))

					else:
						return removeSession()
				except:
					return removeSession()
			else:
				return redirect(url_for('Calificaciones'))
	else:
		return removeSession()
"""
	Ruta para consultar el grupo, exclusiva para tutores, si intentan redireccionar y son alumnos, cierra su 
	sesión y manda al index
"""
@app.route('/home_tutor/grupo', methods=['GET','POST'])
def AltaGrupo():
	if request.method == 'GET':
		try:
			nombreTutor =  session['nombre']
			password = session['password']
			result_tutores = db_session.query(RegistroTutor).filter(RegistroTutor.usuario == nombreTutor).filter(RegistroTutor.contraseña ==  password).first()
			if(result_tutores == None):
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
		
"""
	Ruta para las lecturas complementarias
"""
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
				return removeSession()
			elif 'menuC_button' in request.form:
				nombre =  session['nombre']
				password = session['password']
				#Validamos que exista la sesión para redireccionamientos
				result_tutores = db_session.query(RegistroTutor).filter(RegistroTutor.usuario == nombre).filter(RegistroTutor.contraseña ==  password).first()
				result_alumnos = db_session.query(RegistroAlumno).filter(RegistroAlumno.usuario == nombre).filter(RegistroAlumno.contraseña ==  password).first()
				#Si no existe una sesión con esos datos en la bdd regresamos al index y borramos la sesión
				if(result_tutores == None and result_alumnos == None):
					return removeSession()
				elif(result_alumnos != None or result_tutores != None):
					return redirect(url_for('Complementarias'))
				
				else:
					return removeSession()
					
			elif 'lecturaC2_button' in request.form:
				return redirect(url_for('Complementaria02'))
			elif 'lecturaC3_button' in request.form:
				return redirect(url_for('Complementaria03'))
			else:
				return redirect(url_for('Complementaria01'))
		else:
			return removeSession()
"""
	Ruta para las lecturas complementarias
"""
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
				return removeSession()
			elif 'menuC_button' in request.form:
				nombre =  session['nombre']
				password = session['password']
				#Validamos que exista la sesión para redireccionamientos
				result_tutores = db_session.query(RegistroTutor).filter(RegistroTutor.usuario == nombre).filter(RegistroTutor.contraseña ==  password).first()
				result_alumnos = db_session.query(RegistroAlumno).filter(RegistroAlumno.usuario == nombre).filter(RegistroAlumno.contraseña ==  password).first()
				#Si no existe una sesión con esos datos en la bdd regresamos al index y borramos la sesión

				if(result_tutores == None and result_alumnos == None):
					return removeSession()
				elif(result_alumnos != None or result_tutores != None):
					return redirect(url_for('Complementarias'))
				
				else:
					return removeSession()
				
			elif 'lecturaC1_button' in request.form:
				return redirect(url_for('Complementaria01'))
			elif 'lecturaC3_button' in request.form:
				return redirect(url_for('Complementaria03'))
			else:
				return redirect(url_for('Complementaria02'))
	else:
		return removeSession()
"""
	Ruta para las lecturas complementarias
"""
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
				return removeSession()
			elif 'menuC_button' in request.form:
				nombre =  session['nombre']
				password = session['password']
				#Validamos que exista la sesión para redireccionamientos
				result_tutores = db_session.query(RegistroTutor).filter(RegistroTutor.usuario == nombre).filter(RegistroTutor.contraseña ==  password).first()
				result_alumnos = db_session.query(RegistroAlumno).filter(RegistroAlumno.usuario == nombre).filter(RegistroAlumno.contraseña ==  password).first()
				#Si no existe una sesión con esos datos en la bdd regresamos al index y borramos la sesión
				if(result_tutores == None and result_alumnos == None):
					return removeSession()
				elif(result_alumnos != None or result_tutores != None):
					return redirect(url_for('Complementarias'))
				
				else:
					return removeSession()
			elif 'lecturaC1_button' in request.form:
				return redirect(url_for('Complementaria01'))
			elif 'lecturaC3_button' in request.form:
				return redirect(url_for('Complementaria03'))
			else:
				return redirect(url_for('Complementaria02'))
	else:
		return removeSession()
"""
	Método para guardar las calificaciones de la actividad correspondiente en la base de datos, 
	filta por numero de actividad considerando que la lectura 1 2 y 3 de la unidad 1 son la actividad_1, 
	actividad_2, actividad_3 en la base , por igual la lectura 1 2 y 3 de la unidad 2 son la actividad_4, 
	activdiad_5, actividad_6.

"""
@app.route('/calif-lectura', methods=['GET', 'POST'])
def Califica():
	#Si intentan acceder por GET mandamos un http 403 permiso denegado
	if request.method == 'GET':
		return abort(403)
	#Si recibimos una petición POST entramos aquí
	if request.method == 'POST':
		#Checamos una sesión válida 
		if 'nombre' in session:
			nombre =  session['nombre']
			password = session['password']
			result_tutores = db_session.query(RegistroTutor).filter(RegistroTutor.usuario == nombre).filter(RegistroTutor.contraseña ==  password).first()
			result_alumnos = db_session.query(RegistroAlumno).filter(RegistroAlumno.usuario == nombre).filter(RegistroAlumno.contraseña ==  password).first()
			#Validamos si es tutor , de ser así entonces mandamos un 403 http y redireccionamos al menú obligatorias
			if(result_tutores != None):
				return redirect(url_for('Obligatorias'))
			#En otro caso garantizamos que es un alumno entonces empezamos el parseo de los datos del request
			elif(result_alumnos != None):
				p = db_session.query(Alumno).join(RegistroAlumno).filter(Alumno.idregistroalumno == RegistroAlumno.idregistroalumno).filter(RegistroAlumno.usuario == nombre).filter(RegistroAlumno.contraseña ==  password).first()
				d = db_session.query(GrupoAlumno).join(Alumno).filter(GrupoAlumno.idalumno == Alumno.idalumno).filter(Alumno.idalumno == p.idalumno ).first()
				#Obtenemos el grupo del alumno y su id
				data = request.get_data(parse_form_data=False,  as_text=True) #Obtenemos los datos del request como cadena
				#Parseo de cadenas 
				parseAux01 = data[0:15] 
				
				
				parseAuxCalif = parseAux01[13:15]
				
				calificacionFinal = int(parseAuxCalif)
				parseAux02 = data[16:26]
				
				
				parseLectNum = parseAux02[8:10]
				lectFinal = int(parseLectNum)
				

				parseAux03 = data[27:]
				parseAuxUnidad = parseAux03[7:9]
				unidadFinal = int(parseAuxUnidad)
				#Una vez obtenido el número de lectura y la calificación buscaremos el registro con el alumno en la tabla Actividad
				consultaRegistroActividad = db_session.query(Actividad).filter(Actividad.idalumno == d.idalumno).filter(Actividad.idgrupo == d.idgrupo).first()
				#Como desde el registro ya habíamos agregado, entonces solo debemos actualizar 
				if(consultaRegistroActividad != None):
					string_campo = "actividad_" + str(lectFinal)
					cal = calificacionFinal
					loc = db_session.query(Actividad).filter(Actividad.idalumno == d.idalumno).filter(Actividad.idgrupo == d.idgrupo).first()
					#Ésto simula el switch_case con base en el número de lectura establecido en la descripción del método
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
				return removeSession()
		else:
			return removeSession()

#Función mágica para ejecutar el archivo, manda llamar al método principal main()
if __name__ == '__main__':
	app.run(port = 3000, debug = True)
