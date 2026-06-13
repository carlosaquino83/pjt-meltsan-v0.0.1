GEMINI

-----------------------------------------------------------

PgBouncer es una de las herramientas más críticas y salvavidas cuando quieres exprimir el máximo rendimiento de un servidor PostgreSQL económico.

Aquí te explico a fondo cómo funciona, cómo se instala y qué relación tiene con Python.

1. ¿Cómo funciona PgBouncer?
Por defecto, PostgreSQL utiliza una arquitectura de un proceso por conexión. Si 500 usuarios se conectan a tu ERP al mismo tiempo, Postgres abrirá 500 procesos independientes en tu servidor Linux. Como cada proceso consume entre 2 MB y 10 MB de RAM, el servidor se quedará sin memoria rápidamente y el CPU se saturará cambiando de un proceso a otro.

PgBouncer es un "Pooler" (gestor/concentrador) de conexiones ligero. Se coloca en medio de tu aplicación web y tu base de datos PostgreSQL.

Hacia la aplicación: PgBouncer simula ser una base de datos PostgreSQL normal. Tu aplicación puede abrir 2,000 conexiones simuladas hacia PgBouncer (las cuales casi no consumen RAM porque PgBouncer es ultra eficiente).

Hacia PostgreSQL: PgBouncer mantiene un grupo muy pequeño y fijo de conexiones reales abiertas hacia Postgres (por ejemplo, solo 20 o 30 conexiones).

La magia (Transaction Pooling): Cuando el backend de tu aplicación ejecuta una consulta SQL rápida para la Empresa A, PgBouncer toma una de esas 30 conexiones reales, le entrega la consulta a Postgres, recibe el resultado, se lo devuelve a la aplicación y en ese mismo microsegundo libera la conexión para que pueda ser usada por una consulta de la Empresa B. Postgres nunca se entera de que hay miles de usuarios afuera; solo ve 30 conexiones trabajando a máxima velocidad de forma constante.

2. ¿Se usa Python con PgBouncer?
No para que PgBouncer funcione por dentro, pero SÍ en tu aplicación.

Por dentro: PgBouncer está escrito puramente en C. Está diseñado para ser extremadamente rápido, directo al grano y consumir una cantidad ridícula de memoria RAM (unos cuantos megabytes para gestionar miles de conexiones). No requiere Python, Java ni Node.js para correr.

En tu desarrollo: Tu backend (que perfectamente puede estar escrito en Python usando frameworks como Django o FastAPI, o scripts de conexión con librerías como psycopg2 o asyncpg) se conectará a PgBouncer en lugar de conectarse directamente a Postgres.

Para tu código Python, es completamente transparente: solo cambias el número de puerto en tu configuración (Postgres usa el puerto 5432 por defecto, y PgBouncer suele usar el 6432).

3. ¿Cómo se instala y configura en Linux (Ubuntu/Debian)?
Al estar en un servidor VPS económico con Linux, la instalación es sumamente sencilla porque ya viene en los repositorios oficiales.

-----------------------------------------------------------

Paso 1: Instalación
Entra a la terminal de tu servidor y ejecuta:

        sudo apt update
        sudo apt install pgbouncer

Paso 2: Configurar las conexiones (/etc/pgbouncer/pgbouncer.ini)
Abres el archivo de configuración principal. Ahí le dices a qué base de datos real debe apuntar y en qué puerto va a escuchar:

        [databases]
        # Sintaxis: bd_simulada = host=IP_POSTGRES port=5432 dbname=bd_real
        * = host=127.0.0.1 port=5432

        [pgbouncer]
        logfile = /var/log/postgresql/pgbouncer.log
        pidfile = /var/run/postgresql/pgbouncer.pid

        # Puerto donde escuchará PgBouncer (tu app se conectará aquí)
        listen_port = 6432
        listen_addr = *

        # El secreto del ahorro de RAM: Modo Transacción
        pool_mode = transaction

        # Parámetros de rendimiento para tu servidor económico
        max_client_conn = 2000   # Cuántas conexiones de apps permite afuera
        default_pool_size = 30   # Cuántas conexiones reales mantiene abiertas hacia Postgres

Paso 3: Configurar los usuarios autorizados (/etc/pgbouncer/userlist.txt)
PgBouncer necesita saber qué usuarios tienen permitido loguearse. Creas un archivo con el formato "usuario" "contraseña":

        "admin_erp" "mi_password_seguro"
        "usuario_empresa1" "otro_password"

Paso 4: Iniciar el servicio
Finalmente, habilitas y arrancas el servicio para que se quede corriendo de fondo en tu servidor Linux:

        sudo systemctl enable pgbouncer
        sudo systemctl start pgbouncer

Resumen de beneficios para tu proyecto de 5,000 empresas:
Al implementar PgBouncer en tu arquitectura Multi-esquema de Postgres:

Tu servidor no explotará: Podrás soportar picos de tráfico masivos de múltiples empresas interactuando a la vez.

El "search_path" funciona perfecto: Como usas el modo transaction, tu código Python o Node.js puede enviar el comando SET search_path TO empresa_X; justo antes de cada consulta, asegurando que los datos se mantengan aislados por esquema sin que se mezclen entre transacciones de otros usuarios.
