drop table actividad,  alumno, grupo, grupo_alumno,  registro_tutor, registro_alumno, tutor, tutor_correo;
insert into registro_tutor (usuario, contraseña) values ('don feliz', 'dbed1d1417a60d4d705689cfb8f6051e25f4e089a8eadcff724b60eef5681bd320a5a462de9e66c73ac650c5d96dda3595da79a8feb69679feafa045e5dc44a96881a2441117dc22b5d9fbb11fed27807c13113221e4d477e7f2336212af5f56');
insert into registro_alumno (usuario, contraseña) values ('alexis', 'f5fa60d18560eef8cfc41157426c07a6ae0a26476ac8973ca3198c6fa203cb186f5cc257c5b4645acba60e8d2ebf1c29f890b68a260574df513e2cdbadd602a90b0525cee52f21d6133099df3b93945187f7282b9691ff7e2baddb28546ccbfa');
select *  from registro_alumno;

insert into alumno(idRegistroAlumno, nombre) values (1,'Alexis');
--insert into alumno(idRegistroAlumno, nombre) values (1,'Juan');
select *  from alumno;

insert into tutor (idRegistroTutor, nombre, aPaterno, aMaterno, fNacimiento ) values (1, 'Luis', 'Rey', 'Reynosa', '1990-05-20');
select * from tutor;

insert into grupo(idGrupo,idTutor) values ('G2020-1%@L', 1);
select *  from grupo;
--insert into grupo(idTutor) values (1);
insert into grupo_alumno(idGrupo, idAlumno) values ('G2020-1%@L',1);
select *  from grupo_alumno;

insert into actividad(idGrupo,idAlumno, actividad_1) values ('G2020-1%@L',1,10);
select * from actividad;

CREATE TABLE registro_Tutor(
	idRegistroTutor SERIAL,
	usuario VARCHAR(64) UNIQUE,
	contraseña VARCHAR(256) NOT NULL,	
	CONSTRAINT registro_Tutor_PK PRIMARY KEY (idRegistroTutor)
);

CREATE TABLE tutor(
	idTutor SERIAL,
	idRegistroTutor SERIAL UNIQUE REFERENCES registro_Tutor(idRegistroTutor),
	nombre VARCHAR(64) NOT NULL,
	aPaterno VARCHAR(64) NOT NULL,
	aMaterno VARCHAR(64) NOT NULL,
	fInscripcion DATE  DEFAULT CURRENT_DATE,
	fNacimiento DATE NOT NULL,
	CONSTRAINT tutor_PK PRIMARY KEY (idTutor)
);


CREATE TABLE grupo(
	idGrupo varchar(10) PRIMARY KEY,
    nombreGrupo varchar(32)  NULL ,
	idTutor SERIAL UNIQUE REFERENCES tutor(idTutor)
);

CREATE TABLE registro_Alumno (
	idRegistroAlumno SERIAL,
	usuario VARCHAR(64) UNIQUE NOT NULL,
	contraseña VARCHAR(256) NOT NULL,
	
	CONSTRAINT registro_alumno_PK PRIMARY KEY (idRegistroAlumno)
);

CREATE TABLE alumno(
	idAlumno SERIAL,
	idRegistroAlumno SERIAL UNIQUE REFERENCES registro_Alumno (idRegistroAlumno),
	nombre VARCHAR(64) NOT NULL,
	fInscripcion DATE DEFAULT CURRENT_DATE,

	CONSTRAINT alumno_PK PRIMARY KEY (idAlumno)
);

CREATE TABLE grupo_alumno(
	autoId SERIAL PRIMARY KEY ,
	idGrupo varchar(10)  REFERENCES grupo(idGrupo), 
    idAlumno SERIAL UNIQUE REFERENCES alumno(idAlumno)
);

CREATE TABLE tutor_correo(
	idTutor SERIAL REFERENCES tutor(idTutor),
	correoElectronico VARCHAR(255) UNIQUE,
	
	CONSTRAINT tutor_correo_PK PRIMARY KEY (idTutor, correoElectronico)
);


CREATE TABLE actividad(
	idGrupo varchar(10) REFERENCES grupo(idGrupo),
	idAlumno SERIAL UNIQUE REFERENCES alumno(idAlumno),
	actividad_1 smallint DEFAULT 0,
	actividad_2 smallint DEFAULT 0,
	actividad_3 smallint DEFAULT 0,
	actividad_4 smallint DEFAULT 0,
	actividad_5 smallint DEFAULT 0,
	actividad_6 smallint DEFAULT 0,
	CONSTRAINT actividad_PK PRIMARY KEY (idAlumno)
);
select *  from registro_alumno
select *  from alumno
select * from grupo_alumno;
select *  from actividad;