#!/bin/bash
set -e

IMAGE_NAME="evaluacion2-chile"
CONTAINER_NAME="samplerunning"

API_BASE_URL="${API_BASE_URL:-https://mindicador.cl/api}"
API_TIMEOUT="${API_TIMEOUT:-10}"
PRESUPUESTO_CLP="${PRESUPUESTO_CLP:-1500000}"
API_TOKEN_CHILE="${API_TOKEN_CHILE:-}"

cat > Dockerfile <<'EOF'
FROM python:3.8.2-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

CMD ["python", "app.py"]
EOF

docker stop "$CONTAINER_NAME" 2>/dev/null || true
docker rm "$CONTAINER_NAME" 2>/dev/null || true

docker build -t "$IMAGE_NAME" .

docker run --name "$CONTAINER_NAME" \
  -e API_BASE_URL="$API_BASE_URL" \
  -e API_TIMEOUT="$API_TIMEOUT" \
  -e PRESUPUESTO_CLP="$PRESUPUESTO_CLP" \
  -e API_TOKEN_CHILE="$API_TOKEN_CHILE" \
  "$IMAGE_NAME"

mkdir -p evidencias/docker

{
  echo "===== docker ps -a ====="
  docker ps -a
  echo ""
  echo "===== logs del contenedor ====="
  docker logs "$CONTAINER_NAME"
} > evidencias/docker/output.txt

echo "Archivo generado: evidencias/docker/output.txt"
