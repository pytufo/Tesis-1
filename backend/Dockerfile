# Usar una imagen de Python como base
FROM python:3.11.4-slim-buster
# Establecer el directorio de trabajo
WORKDIR /usr/src/app

# Definir las variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalar dependencias de sistema
RUN apt-get update && apt-get install -y netcat


# Instalar las dependencias del proyecto
RUN pip install --upgrade pip
COPY ./requirements.txt  .
RUN pip install -r requirements.txt

#
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# Copiar el proyecto en el contenedor
COPY . .

ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]

# Configurar variables de entorno si es necesario
#ENV DJANGO_SETTINGS_MODULE=bibloteca.settings
#ENV SECRET_KEY=django-insecure-=v7mh$lumcn$l!=$qcql+aaq^$#&g(k6zhg-b&ev*-q94cft+v

# Realizar las migraciones y arrancar el servidor
#RUN python manage.py migrate
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
