#!/bin/bash

# Ruta donde guardar los workflows exportados
WORKFLOW_DIR="/opt/n8n/workflows"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Crear la carpeta de destino si no existe
mkdir -p "$WORKFLOW_DIR"

# Elimina antiguos exports automáticos (opcional, deja sólo los últimos 10 backups)
ls -tp $WORKFLOW_DIR/export_*.json | grep -v '/$' | tail -n +11 | xargs -I {} rm -- {}

# Exporta todos los workflows en un único JSON
docker exec n8n-main n8n export:workflow --all --output="/home/node/exported_workflows/export_${TIMESTAMP}.json"

# Copia desde el volumen del contenedor a la carpeta del host
docker cp n8n-main:/home/node/exported_workflows/. $WORKFLOW_DIR/

# Añade y commitea
git add workflows
git commit -m "Backup workflows $TIMESTAMP"

echo "✅ Backup de workflows exportado, copiado y versionado en Git correctamente: $WORKFLOW_DIR/export_${TIMESTAMP}.json"
