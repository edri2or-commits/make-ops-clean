FROM node:18

WORKDIR /usr/src/app

COPY package.json ./
RUN npm install --only=production

COPY index.js ./

ENV PORT=8080
EXPOSE 8080

CMD ["npm", "start"]
