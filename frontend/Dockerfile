# $ ---------- Base Stage ----------
FROM node:24.11.0-alpine3.22 AS base
WORKDIR /app
COPY package*.json ./

# $ ---------- Development Stage ----------
FROM base AS dev
ENV NODE_ENV=development
RUN npm install
COPY . .
CMD ["npm", "run", "dev"]

# $ ---------- Production Stage ----------
FROM base AS prod
ENV NODE_ENV=production
RUN npm ci --only=production && npm cache clean --force
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["sh", "-c", "npm", "run", "start"]
