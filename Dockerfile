# Imagen de producción de un solo servicio: FastAPI entrega la API y la interfaz compilada (mismo origen,
# requisito de las cookies HttpOnly + SameSite=Strict). Se compila en el hosting; no hace falta Docker local.

FROM node:22-alpine AS interfaz
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
# La interfaz llama a la API con ruta relativa porque ambas viven en el mismo origen.
ENV VITE_API_URL=/api/v1
RUN npm run build

FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app
COPY backend/requirements.txt backend/requirements.txt
RUN pip install -r backend/requirements.txt
COPY backend backend
COPY database database
COPY deploy/arranque.sh deploy/arranque.sh
COPY --from=interfaz /app/frontend/dist frontend/dist
RUN useradd --system --no-create-home eco && chown -R eco /app/backend
USER eco
WORKDIR /app/backend
ENV FRONTEND_DIST=/app/frontend/dist COOKIE_SECURE=true
EXPOSE 8000
CMD ["sh", "../deploy/arranque.sh"]
