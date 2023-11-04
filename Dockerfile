# Usar una imagen de Python como base
FROM python:3.9

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requisitos
COPY requirements.txt /app/

# Instalar las dependencias del proyecto
RUN pip install -r requirements.txt

# Copiar el proyecto en el contenedor
COPY . /app/

# Configurar variables de entorno si es necesario
ENV DJANGO_SETTINGS_MODULE=bibloteca.settings
ENV SECRET_KEY=django-insecure-=v7mh$lumcn$l!=$qcql+aaq^$#&g(k6zhg-b&ev*-q94cft+v

# Realizar las migraciones y arrancar el servidor
RUN python manage.py migrate
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]