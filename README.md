Visión general
Demostración de aplicación

Dependencies
Python 3.5
Django 4.0.7
React 17.0.2

Instalación

Download/clone repo.

Paso 1: Poner en funcionamiento Django Rest Framework Backend

- Cree un entorno virtual para el backend llamado 'env'

    python -m venv env
    python3 -m venv env

- Activarlo
    Windows
        -   cd env\Scripts
    Linux
        -   source env/bin/activate

- Requisitos de instalación después de crear y activar el entorno virtual

    $ pip install -r requirements/local.txt

- Revisar archivo .env en la configuración y poner variables para la clave secreta y la base de datos (PostgreSQL) son opcionales por defecto está configurado en IS_POSTGRESQL = Falso. Si convierte esto en  True o Verdadero, configure las variables que se detalla a continuación:
    SECRET_KEY=some-secret-key
    DATABASE_ENGINE=django.db.backends.postgresql_psycopg2
    DATABASE_NAME=*******
    DATABASE_USER=*******
    DATABASE_PASS=*******
    DATABASE_HOST=localhost
    DATABASE_PORT=5432

- Una vez configurado el archivo se debe ejecutar los siguientes comandos para poder migrar las tablas a la base de datos configurada.

    $ python manage.py realizar migraciones
    $ python administrar.py migrar

    Creación de super usuario para el administrador de Django
    Ejecutar el comando
    $ python manage.py createsuperuser
    Complete el nombre de usuario, correo electrónico y contraseña para el superusuario (administrador)

Para ejecutar UnitTests:
    $ python administrar.py prueba

- Por último se debe ejecutar el comando que se detalla a continuación para poder iniciar el backend de la aplicación.
    $ python manage.py runserver
La documentación de las API's estará disponible en `http://localhost:8000/api/v1/docs/`

Administrador disponible en `http://localhost:8000/admin/`


Paso 2: Poner en funcionamiento React JS Frontend
- Ingrese a la carpeta frontend del proyecto.
- Instale dependencias en la aplicación frontend usando el siguiente comando en una terminal.
    $ npm install
- Primero asegúrese de haber instalado Node.js. mientras actualiza esta configuración.

- Luego ejecute los siguientes comandos en el directorio frontend

    $ npm start

- Aplicación React disponible en `http://localhost:3000/`