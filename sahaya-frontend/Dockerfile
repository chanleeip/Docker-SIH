FROM node:current-alpine3.18
WORKDIR /frontend
COPY . .
RUN npm install
RUN npm install -g expo-cli
CMD [ "expo","start" ]