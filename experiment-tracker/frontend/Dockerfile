FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
```

**docker-compose.yml:**

Na raiz do projeto, copie tudo do artifact intitulado "Docker Compose - ExperimentVault"

**Resumo de arquivos:**
```
backend/Dockerfile          ← Backend
frontend/Dockerfile        ← Frontend
docker-compose.yml         ← Raiz do projeto