FROM node:16

WORKDIR /app

RUN npm install express mongodb

COPY app /app

EXPOSE 3000

CMD ["node", "app.js"]
