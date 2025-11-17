FROM node:18-slim

WORKDIR /usr/src/app

COPY package*.json ./
RUN npm install --omit=dev

COPY . .

ENV PORT=8080
EXPOSE 8080

CMD ["npm", "start"]  # Fixed: was CLM (typo), now CMD (correct Docker directive)