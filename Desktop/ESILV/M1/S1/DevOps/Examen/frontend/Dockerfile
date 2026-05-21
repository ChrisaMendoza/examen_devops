FROM node:22-alpine
WORKDIR /app
COPY package*.json ./
RUN npm run dev
COPY . .
EXPOSE 3000
CMD ["node", "index.js"]