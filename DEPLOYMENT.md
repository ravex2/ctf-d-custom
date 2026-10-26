# Publicación local con Cloudflare Tunnel

Esta configuración ejecuta CTFd, MariaDB y Redis en este computador. Sus
datos quedan en `.data/`, que se debe respaldar. El único puerto publicado es
`127.0.0.1:8000`; no se expone ningún servicio al router o a Internet.

## Primera configuración

1. Copia la plantilla de secretos:

   ```sh
   cp .env.example .env
   ```

2. Genera tres secretos distintos y pégalos en `.env`:

   ```sh
   openssl rand -hex 32
   ```

   Usa uno para `CTFD_SECRET_KEY`, uno para `MARIADB_ROOT_PASSWORD` y uno
   para `MARIADB_PASSWORD`. No uses espacios ni caracteres como `@`, `:` o
   `/` en la contraseña de MariaDB, porque forma parte de una URL.

3. En Cloudflare Zero Trust, crea un túnel de tipo **Cloudflared**. Durante
   la instalación elige Docker y copia el valor que aparece después de
   `--token`; pégalo como `CLOUDFLARE_TUNNEL_TOKEN` en `.env`.

4. En la ruta pública del túnel, crea el hostname que usarán los jugadores,
   por ejemplo `ctf.tudominio.cl`, y apunta el servicio a:

   ```text
   http://nginx:80
   ```

   Ese nombre funciona porque `cloudflared` y Nginx comparten la red Docker.

## Inicio

```sh
docker compose up -d --build
docker compose ps
```

Abre `http://localhost:8000` para completar el asistente inicial de CTFd.
Cuando hayas configurado el token, inicia el túnel:

```sh
docker compose --profile tunnel up -d
```

Cuando el túnel aparezca como **Healthy** en Cloudflare, usa
`https://ctf.tudominio.cl` para el acceso público. El perfil evita que un
token aún no configurado bloquee la prueba local de CTFd.

## Operación

```sh
# Ver registros
docker compose logs -f ctfd cloudflared

# Detener sin borrar datos
docker compose down

# Reiniciar tras un cambio
docker compose up -d --build
```

No ejecutes `docker compose down -v`: eliminaría los volúmenes nombrados.
Los datos principales en esta configuración son bind mounts bajo `.data/`;
respalda esa carpeta antes y después del evento.

## Recuperación y seguridad

- Mantén el equipo encendido y sin suspensión durante el CTF.
- No abras los puertos 8000, 80, 3306 ni 6379 en el router.
- Conserva una copia privada de `.env` y del respaldo de `.data/`.
- El acceso administrativo de CTFd se configura en su asistente inicial; usa
  una contraseña distinta y robusta.
