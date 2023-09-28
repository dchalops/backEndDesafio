# Usa una imagen base de Python
FROM python:3.9

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt al directorio de trabajo
# Copia el archivo requirements/production.txt al directorio de trabajo
COPY requirements/production.txt /app/requirements/production.txt

# Instala las dependencias de la aplicación
RUN pip install --no-cache-dir -r /app/requirements/production.txt

# Copia el contenido de la aplicación actual al directorio de trabajo
COPY . /app/

# Configura las variables de entorno (puedes personalizar estas según tus necesidades)
ENV DJANGO_SETTINGS_MODULE=myproject.settings
ENV DEBUG=False

# Expone el puerto en el que se ejecuta la aplicación (ajusta esto según tu configuración)
EXPOSE 8000

# Comando para ejecutar la aplicación cuando se inicie el contenedor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
