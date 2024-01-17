FROM node:18-buster-slim

ARG NODE_ENV=production
ENV NODE_ENV $NODE_ENV

ARG PORT=19006
ENV PORT $PORT
EXPOSE $PORT

# Crear directorio de la aplicación
WORKDIR /opt/frontend/app

# Copiar solo los archivos de configuración necesarios
COPY ./package.json ./package-lock.json ./

# Instalar dependencias
RUN npm install

# Copiar el resto de la aplicación
COPY . .

# Entrypoint para iniciar la aplicación
ENTRYPOINT [ "npm", "run", "web" ]