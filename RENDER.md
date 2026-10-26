# Despliegue en Render

Esta alternativa usa una sola instancia de CTFd y un disco SSD persistente de
Render. No usa MariaDB ni Redis: CTFd guarda usuarios, puntajes, archivos y
cache en SQLite dentro del disco. Es apropiada para un CTF de reversing de
baja concurrencia, con una única instancia.

## Costo y límites

El Blueprint usa el plan `0.5c-512mb` y un disco de 1 GB: es el mínimo pagado
de Render. El plan tiene 512 MB de RAM, por debajo del mínimo de 1 GB que
recomienda CTFd; úsalo sólo tras probarlo con los challenges reales. Si se
queda sin memoria o hay lentitud, cambia el plan a `1c-2g` desde Render.

Render no ofrece discos persistentes para servicios gratuitos, por lo cual su
plan Free no sirve para mantener la base SQLite ni los binarios entre
reinicios.

## Crear el servicio

1. Sube este repositorio a un repositorio Git al que Render tenga acceso.
2. En Render, selecciona **New > Blueprint** y elige ese repositorio. Render
   detectará `render.yaml`.
3. Revisa el nombre del servicio, crea el Blueprint y espera a que termine el
   primer deploy.
4. Abre la URL `https://ctfd-reversing.onrender.com` que Render muestra en el
   panel y completa el asistente inicial de CTFd.
5. Si tienes dominio, agrégalo en la sección **Settings > Custom Domains** del
   servicio. Render gestiona TLS automáticamente.

Render genera y almacena `SECRET_KEY` en secreto durante el primer despliegue;
no hay que copiarla a Git ni modificarla después, ya que invalidaría las
sesiones existentes.

## Datos y respaldo

Todo lo que debe persistir está bajo `/opt/CTFd/.data` en el disco de Render:

- `ctfd.db`: base SQLite con usuarios, flags y scoreboard.
- `uploads/`: binarios y adjuntos de los challenges.
- `logs/` y `filesystem_cache/`: registros y cache de CTFd.

El servicio debe mantenerse en una sola instancia: un disco persistente no se
comparte entre réplicas. Antes del evento y al terminarlo, descarga una copia
del disco mediante la Shell/SFTP de Render o usa su snapshot diario como
respaldo adicional.

## Operación

Cada push a la rama conectada crea un deploy. Al tener un disco, Render detiene
la instancia anterior antes de activar la nueva; habrá unos segundos de
indisponibilidad. Programa los cambios fuera del horario del CTF.

Para depurar, revisa los logs del servicio en el panel de Render. Para subir
binarios, usa la interfaz de administración de CTFd; se guardarán en el disco
persistente.
