# Proyecto n8n Autoalojado (Docker + Backup Automático + GitHub)

Repositorio profesional para desplegar, mantener y versionar una instancia de **n8n** autoalojada usando Docker Compose, backups automáticos de workflows y control de versiones con Git y GitHub.

## Índice
1. Descripción del proyecto
2. Infraestructura
3. Requisitos previos
4. Instalación paso a paso
5. Automatización de backups de Workflows
6. Estructura del repositorio
7. Buenas prácticas y seguridad
8. Colaboración y despliegue
9. Contacto

## Descripción del proyecto

Este repositorio está diseñado para:

- Desplegar n8n de forma segura y escalable con Docker Compose.
- Gestionar backups automáticos de workflows (exportación diaria/semanal en JSON).
- Versionar la configuración y los workflows en Git y GitHub.
- Preparar entornos para múltiples usuarios y equipos.

## Infraestructura

- **Docker Compose:** n8n, PostgreSQL, Redis, Traefik (reverse proxy y SSL con Let's Encrypt).
- **Volúmenes persistentes:** para datos, workflows y certificados.
- **Scripts automáticos:** para exportación y backup.
- **Git:** para versionado de infraestructura y workflows exportados.

## Requisitos previos

- VPS/servidor propio (por ejemplo, Digital Ocean, AWS, etc).
- Docker y Docker Compose instalados.
- Git instalado.
- Acceso a un dominio para configurar Traefik y SSL.

## Instalación paso a paso

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/TU_REPO.git
cd TU_REPO
```

### 2. Copiar y configurar el archivo .env

Copia el archivo de ejemplo y edita los valores:

```bash
cp .env.example .env
nano .env
```
IMPORTANTE: Nunca subas tu `.env` real a GitHub. Está protegido por `.gitignore`.

### 3. Revisar y adaptar docker-compose.yml

El archivo `docker-compose.yml` utiliza variables de entorno del `.env`. Asegúrate de que los paths y variables coinciden con tu entorno.

### 4. Permisos y volúmenes

Antes de levantar los servicios, otorga permisos correctos:

```bash
sudo chown -R 1000:1000 ./data ./postgres-data ./postgres-extras-data ./workflows
sudo chmod -R 700 ./data ./postgres-data ./postgres-extras-data ./workflows
```

### 5. Crear red externa (si usas Traefik)

```bash
docker network create traefik
```

### 6. Levantar los servicios

```bash
docker-compose up -d
```

Accede a n8n en tu dominio:

```
https://TUDOMINIO.COM
```

## Automatización de backups de Workflows

### Backup automático de workflows

Todos los días (o semana, según tu `crontab`) se exportan los workflows y se almacenan en `/opt/n8n/workflows`.

Puedes versionar los backups en Git con un simple commit y push.

### Script de exportación

Ruta: `/opt/n8n/scripts/export_workflows.sh`  
(Ejemplo incluido en este repo)

Hazlo ejecutable:

```bash
chmod +x /opt/n8n/scripts/export_workflows.sh
```

Ejecuta manualmente con:

```bash
/opt/n8n/scripts/export_workflows.sh
```

Configura el cron:

```bash
crontab -e
# Ejemplo para cada día a las 03:30 AM
30 3 * * * /opt/n8n/scripts/export_workflows.sh >> /opt/n8n/scripts/cron_export.log 2>&1
```

## Estructura del repositorio

```
/data                   # Configuración y datos persistentes de n8n
/workflows              # Backups automáticos exportados de workflows (JSON)
/letsencrypt            # Certificados SSL automáticos de Traefik (no subir)
/postgres-data          # Datos de PostgreSQL n8n (no subir)
/postgres-extras-data   # Datos de PostgreSQL extra (no subir)
/scripts                # Scripts automáticos para backup, etc.
docker-compose.yml      # Infraestructura principal
.env                    # Configuración sensible (no subir)
.env.example            # Plantilla de variables de entorno
.gitignore              # Exclusiones para archivos sensibles y grandes
README.md               # Esta documentación
```

## Buenas prácticas y seguridad

- `.env` siempre en el `.gitignore`: ¡Nunca subas tus credenciales!
- Regenera los tokens/contraseñas antes de compartir el repo.
- Haz `git pull origin main` antes de trabajar para evitar conflictos.
- Si hay cambios remotos, resuélvelos con merge antes de tu push.
- Usa ramas si vas a implementar grandes cambios o nuevas features.

## Colaboración y despliegue

Actualizar tu copia local antes de trabajar:

```bash
git pull origin main
```

Versionar los backups de workflows:

```bash
git add workflows/
git commit -m "Backup automático de workflows [fecha]"
git push origin main
```

## Contacto

Responsable: Julio - Ideasforge
Contacto: julio@ideasforge.io

¿Dudas, mejoras o quieres colaborar? Abre un issue o contacta.

¿Quieres alguna adaptación para un equipo, multi-entorno o integración CI/CD? ¡Dímelo y lo añadimos!
