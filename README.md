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
DATABASE_URL=postgresql+psycopg2://nutribase:nutripass@localhost:5432/nutridb
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

## 🐳 Despliegue con Docker (entorno completo)

```bash
docker compose up --build
```

Esto levanta:

* Backend en `http://localhost:8000`
* Base de datos PostgreSQL

---

# 🚀 Despliegue en Producción

Para producción se recomienda usar **Docker + Nginx + HTTPS**.

## 1️⃣ Variables de entorno

Crear `.env.prod`:

```bash
DATABASE_URL=postgresql+psycopg2://nutribase:password_seguro@db:5432/nutridb
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
