FROM node:18-buster-slim

ARG NODE_ENV=production
ENV NODE_ENV $NODE_ENV

ARG PORT=19006
ENV PORT $PORT
EXPOSE $PORT 19001 19002

ENV NPM_CONFIG_PREFIX=/home/node/.npm-global
ENV PATH /home/node/.npm-global/bin:$PATH

RUN mkdir /opt/frontend
WORKDIR /opt/frontend
ENV PATH /opt/frontend/.bin${PATH}
COPY ./package.json ./package-lock.json ./
RUN npm install

WORKDIR /opt/frontend/app
COPY ./ .

ENTRYPOINT [ "npm", "run" ]
CMD [ "web" ]