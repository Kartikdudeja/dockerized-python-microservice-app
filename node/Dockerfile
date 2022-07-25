FROM node:lts-alpine3.15

WORKDIR /usr/src/app

# Install app dependencies
COPY ./node/package*.json ./

RUN npm install

COPY ./node .

EXPOSE 3000

CMD [ "node", "server.js" ]