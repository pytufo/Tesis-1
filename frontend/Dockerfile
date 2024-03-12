FROM node:18-buster-slim AS builder

# ARG NODE_ENV=production
# ENV NODE_ENV $NODE_ENV

# ARG PORT=19006
# ENV PORT $PORT
# EXPOSE $PORT

# Crear directorio de la aplicación
WORKDIR /opt/frontend/app

# Copiar solo los archivos de configuración necesarios
COPY ./frontend/package.json ./frontend/package-lock.json ./

# Instalar dependencias
RUN npm install expo-cli@latest
RUN npm install

COPY ./frontend .

# Copiar el resto de la aplicación
FROM node:18-buster-slim
WORKDIR /opt/frontend/app
COPY --from=builder /opt/frontend/app .

# Entrypoint para iniciar la aplicación
ENTRYPOINT [ "npx", "expo", "start", "--web"]

