# 🧠 NutriTrace — Backend

API REST desarrollada con **FastAPI** y **SQLAlchemy/SQLModel** que gestiona usuarios, alimentos, comidas y objetivos nutricionales.
Proporciona autenticación mediante **JWT**, validación con **Pydantic** y persistencia en **PostgreSQL**.

---

## 🚀 Tecnologías principales

* 🐍 **FastAPI** → Framework backend moderno y asíncrono
* 🧱 **SQLAlchemy / SQLModel** → ORM y modelo de datos
* 🐘 **PostgreSQL** → Base de datos relacional
* 🔐 **JWT (JSON Web Tokens)** → Autenticación segura
* ⚙️ **Pydantic** → Validación de datos
* 🧪 **Pytest** → Framework de testing
* 🐳 **Docker / Docker Compose** → Contenedorización y despliegue

---

## 🧩 Estructura del proyecto

```plaintext
NutriraceBackend/
├── app/
│   ├── main.py
│   ├── api/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── core/
│   └── db/
├── tests/
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

---

## ⚙️ Instalación y ejecución local

### 🔧 Requisitos

* Python ≥ 3.11
* PostgreSQL ≥ 15
* (Opcional) Docker

### ▶️ Pasos

```bash
git clone https://github.com/AnteroEscuder/NutriraceBackend
cd NutriraceBackend

python -m venv venv
source venv/bin/activate   # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

Crear archivo `.env`:

```bash
DATABASE_URL=postgresql+psycopg2://root:1234@localhost:5432/nutritrace
JWT_SECRET=cambiar_este_secret
CORS_ORIGINS=http://localhost:5173
```

Iniciar servidor:

```bash
uvicorn app.main:app --reload
```

📘 Documentación interactiva:
👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Pruebas automatizadas

```bash
pytest -v
```

Incluye pruebas de autenticación, endpoints y validaciones.

---

## 🐳 Despliegue completo con Docker

Esta opción levanta todo lo necesario para ejecutar la API:

* Backend FastAPI en `http://localhost:8000`
* PostgreSQL 15 en `localhost:5432`
* Volumen persistente para conservar los datos
* Variables de entorno para conectar la API con la base de datos

### 1️⃣ Requisitos

Tener instalados:

* Docker
* Docker Compose

Comprobar instalación:

```bash
docker --version
docker compose version
```

### 2️⃣ Variables de entorno

Crear un archivo `.env` en la raíz del proyecto:

```bash
DATABASE_URL=postgresql+psycopg2://root:1234@db:5432/nutritrace
JWT_SECRET=cambiar_este_secret_por_uno_seguro
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

> Dentro de Docker se usa el host `db`, porque es el nombre del servicio de PostgreSQL en Docker Compose.

Para que Alembic ejecute migraciones dentro de Docker, revisa también `alembic.ini` y usa la misma base de datos con el host `db`:

```ini
sqlalchemy.url = postgresql://root:1234@db:5432/nutritrace
```

Si vas a ejecutar Alembic fuera de Docker, cambia temporalmente el host a `localhost`:

```ini
sqlalchemy.url = postgresql://root:1234@localhost:5432/nutritrace
```

### 3️⃣ Dockerfile del backend

El backend necesita un `Dockerfile` en la raíz del proyecto. Si no existe, créalo con este contenido:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 4️⃣ Docker Compose completo

Para desplegar backend + base de datos, `docker-compose.yml` debe incluir ambos servicios:

```yaml
version: "3.8"

services:
  db:
    image: postgres:15
    container_name: nutritrace_db
    restart: always
    environment:
      POSTGRES_USER: root
      POSTGRES_PASSWORD: 1234
      POSTGRES_DB: nutritrace
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U root -d nutritrace"]
      interval: 5s
      timeout: 5s
      retries: 10

  backend:
    build: .
    container_name: nutritrace_backend
    restart: always
    env_file:
      - .env
    ports:
      - "8000:8000"
    volumes:
      - ./static:/app/static
    depends_on:
      db:
        condition: service_healthy

volumes:
  postgres_data:
```

### 5️⃣ Levantar el entorno

Construir las imágenes y arrancar los contenedores:

```bash
docker compose up -d --build
```

Ver contenedores activos:

```bash
docker compose ps
```

Ver logs del backend:

```bash
docker compose logs -f backend
```

La documentación interactiva queda disponible en:

👉 [http://localhost:8000/docs](http://localhost:8000/docs)

### 6️⃣ Crear tablas y cargar datos iniciales

Ejecutar migraciones de Alembic dentro del contenedor:

```bash
docker compose exec backend alembic upgrade head
```

Cargar alérgenos iniciales:

```bash
docker compose exec backend python scripts/seed_allergens.py
```

Cargar alimentos del sistema:

```bash
docker compose exec backend python scripts/seed_system_foods.py
```

### 7️⃣ Comandos útiles

Parar los contenedores sin borrar datos:

```bash
docker compose down
```

Parar y borrar también el volumen de PostgreSQL:

```bash
docker compose down -v
```

Reconstruir el backend después de cambiar dependencias:

```bash
docker compose up -d --build backend
```

Entrar en una shell del contenedor:

```bash
docker compose exec backend bash
```

Ejecutar tests dentro de Docker:

```bash
docker compose exec backend pytest -v
```

### 8️⃣ Problemas frecuentes

Si el backend no conecta con PostgreSQL, revisa que `DATABASE_URL` use `db` como host:

```bash
DATABASE_URL=postgresql+psycopg2://root:1234@db:5432/nutritrace
```

Si el puerto `5432` ya está ocupado en tu máquina, cambia el puerto publicado de PostgreSQL:

```yaml
ports:
  - "5433:5432"
```

No cambies `db:5432` dentro de `DATABASE_URL`, porque esa conexión ocurre dentro de la red interna de Docker.

---

# 🚀 Despliegue en Producción

Para producción se recomienda usar **Docker + Nginx + HTTPS**.

## 1️⃣ Variables de entorno

Crear `.env.prod`:

```bash
DATABASE_URL=postgresql+psycopg2://root:password_seguro@db:5432/nutritrace
JWT_SECRET=secret_largo_y_seguro
CORS_ORIGINS=https://tudominio.com
ENV=production
```

---

## 2️⃣ Ejecutar en producción

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

El backend debe ejecutarse sin `--reload`:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## 3️⃣ Configurar Nginx (Reverse Proxy)

Ejemplo básico:

```nginx
server {
    listen 80;
    server_name tudominio.com;

    location / {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Esto permite exponer la API mediante tu dominio.

---

## 4️⃣ Activar HTTPS (Let’s Encrypt)

Generar certificado con Certbot:

```bash
certbot certonly --webroot -w /var/www/html -d tudominio.com
```

Configurar Nginx para usar:

```nginx
listen 443 ssl;
ssl_certificate /etc/letsencrypt/live/tudominio.com/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/tudominio.com/privkey.pem;
```

---

## 🔐 Buenas prácticas en producción

* Usar contraseñas seguras para PostgreSQL
* JWT_SECRET largo y privado
* Limitar CORS al dominio real
* No subir archivos `.env` al repositorio
* Realizar backups periódicos de la base de datos

---

## 📦 Endpoints principales

| Método | Ruta           | Descripción          |
| ------ | -------------- | -------------------- |
| POST   | /auth/register | Registro de usuario  |
| POST   | /auth/login    | Login y JWT          |
| GET    | /foods         | Buscar alimentos     |
| GET    | /foods/{id}    | Obtener alimento     |
| POST   | /meals         | Registrar comida     |
| GET    | /meals         | Listar comidas       |
| GET    | /goals         | Ver objetivos        |
| PUT    | /goals         | Actualizar objetivos |

---

## 🧱 Integración con frontend

🔗 [https://github.com/AnteroEscuder/NutritraceFrontend](https://github.com/AnteroEscuder/NutritraceFrontend)

---

## 👩‍💻 Autor

**Antero José Escuder Omenat**
Tutor: Jorge Agustín Barón Abad — IES Polígono Sur

---
