from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
#creamos el motor con la url de la base en postgres
engine = create_engine('postgresql://postgres:1234@localhost/dummy_db', convert_unicode=True, pool_size=10, max_overflow=20)
connection = engine.connect()
#Automapeamos la base con el ORM, así no tenemos que definir todas las tablas manualmente
Base = automap_base()
#Aquí le decimos que haga reflexión de las tablas
Base.prepare(engine, reflect=True)
#Creamos la sessión para consultas a la base, através de ésta hacemos las consultas
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
#Esto no se si sea necesario
Base.query = db_session.query_property()


