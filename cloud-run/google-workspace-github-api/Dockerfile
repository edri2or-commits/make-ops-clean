FROM node:18-slim

# מתקינים אפליקציית Node/Express
WORKDIR /usr/src/app

# מתקינים תלות
COPY package*.json ./
RUN npm install --omit=dev

# מעתיקים את שאר הקבצים (index.js וכו')
COPY . .

# Cloud Run מקשיב על PORT שמוזרק, ברירת מחדל 8080
ENV PORT=8080
EXPOSE 8080

# הפעלת השרת
CMD ["node", "index.js"]
