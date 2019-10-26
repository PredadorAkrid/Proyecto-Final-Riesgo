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
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
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
from models import DummyTable as DummyTable


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

#Vista de bienvenida, primera que cargamos
@app.route("/", methods=['GET', 'POST'])
def Index():
	session.clear()
	if request.method == 'GET':
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
			result = db_session.query(DummyTable).filter(DummyTable.nombre == usuario).filter(DummyTable.contra == password).first()
			#if(len(result) == 0):
			#	return redirect(url_for('/'))
			#else:
			if(result == None):
				return redirect('/')
			else:
				session['nombre'] = usuario
				session['password'] = password
				print(result.nombre)
				print(result.contra)
				return redirect(url_for('Home'))
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
			return redirect('/register') # do something else
		

#Ruta para vista de registro
@app.route('/register', methods=['GET', 'POST'])
def Register():
	if request.method == 'GET':
		return render_template("registro.html")
	elif register.method == 'POST':
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
		#print("Sesión inválida")
		#redirect(url_for('/'))

		#nombre = session['nombre']
		#contra = session['password']
		#print(nombre +  "  asd  " + contra)
		return render_template("home.html");




if __name__ == '__main__':
	app.run(port = 3000, debug = True)
