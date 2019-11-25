# Proyecto-Final-Riesgo
Repositorio para el desarrollo del proyecto final de Riesgo Tecnológico 2020-1

## Integrantes
** Lider de proyecto: Amaya López Dulce Fernanda **  
** Responsable calidad: Sainz Takata Izumi María  **  
** Responsable TI: Navarrete Puebla Alexis  **  
** Programador: Martínez Lechuga Jose Eduardo  **  
** Diseñador: Rosado Cabrera Diego  **  


## Introducción:
Éste proyecto provee una herramienta complementaria para el curso de Inglés, se presentan lecturas y actividades para que los niños lo resuelvan y puedan repasar lo visto en clase.

## Prerequisitos:
* Python3 https://www.python.org/downloads/windows/ --Windows https://www.python.org/downloads/source/ --Linux (Distribuciones Debian)
* Pip3                                                python3 get-pip.py --Linux (Distribuciones Debian)
* Virtualenv                                          pip install virtualenv
* Windows 10 o Linux compatible con python >= 3.0
* Postgresql 10 o superior y PGADMIN4 (opcional)

## Instalación

#### Paso 1 - Clonar el proyecto 

  * git clone https://github.com/PredadorAkrid/Proyecto-Final-Riesgo.git
### Paso 2 - Crear entorno virtual
  #### En entorno windows abrir cmd como administrador e irnos a la ruta del proyecto, ejecutar:
       * virtualenv env
  #### En entorno Linux abrir terminal y repetir los pasos que en windows
### Paso 3 - Activar entorno virtual
  #### En entorno Windows abrir la carpeta env/Scripts y ejecutar el archivo:
       * Activate.bat
  #### En entorno Linux abrir la carpeta env/bin y ejecutar el archivo:
       * activate.sh
### Paso 4 - Ir a la carpeta ProyectoFinalRiesgo y ejecutar el comando:
      * pip3 install -r requirements.txt
### Paso 6 -  Una vez instalado los requerimientos crear la base de datos y restaurar el .sql

### Paso 7 - Ir al archivo database.py y cambiar la url por la url de la base local (usuario contraseña y nombre de la base de datos)

### Paso 8 - Correr el siguiene comando en la carpeta donde se encuentra el archivo app.py
      * python  app-py
### Paso 9 entrar a localhost:3000 y probar las credenciales de prueba:
      * Profesor amaya221 pru3baprof3sor
      * Alumno alexis 4l3xis3schido
## Estructura del proyecto


```
ProyectoFinalRiesgo/
└── app_riesgo/
   ├── pycache/
   ├── static/
       └──css
          └──..
       └──js
          └──..
       └──img
          └──..
   ├── templates/
       └──complementarias/
       └── obligatorias/
       └── index.html
       └──...
   ├──/
       ├── .git
       ├── accounts/
       ├── assets/
       ├── config/
       └── ...
 └── DDL.sql
 └── Readme.md
 └── Licence.txt
```



## License
[APACHE 2.0](https://choosealicense.com/licenses/apache-2.0/)
