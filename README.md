# 🧠 NutriTrace — Backend

API REST desarrollada con **FastAPI** y **SQLAlchemy/SQLModel** que gestiona usuarios, alimentos, comidas y objetivos nutricionales.  
Proporciona autenticación mediante **JWT**, validación con **Pydantic** y persistencia en **PostgreSQL**.

---

## 🚀 Tecnologías principales

- 🐍 **FastAPI** → Framework backend moderno y asíncrono  
- 🧱 **SQLAlchemy / SQLModel** → ORM y modelo de datos  
- 🐘 **PostgreSQL** → Base de datos relacional  
- 🔐 **JWT (JSON Web Tokens)** → Autenticación segura  
- ⚙️ **Pydantic** → Validación de datos  
- 🧪 **Pytest** → Framework de testing  
- 🐳 **Docker / Docker Compose** → Contenedorización y despliegue

---

## 🧩 Estructura del proyecto

```plaintext
NutriraceBackend/
├── app/
│   ├── main.py          # Punto de entrada FastAPI
│   ├── api/             # Routers (auth, users, foods, meals, goals)
│   ├── models/          # Modelos ORM (SQLModel)
│   ├── schemas/         # Modelos Pydantic (entrada/salida)
│   ├── services/        # Lógica de negocio y validaciones
│   ├── core/            # Configuración, seguridad (JWT, bcrypt)
│   └── db/              # Conexión y sesión con la base de datos
├── tests/               # Pruebas automatizadas con Pytest
├── requirements.txt     # Dependencias del proyecto
└── Dockerfile           # Imagen para despliegue
````

---

## ⚙️ Instalación y ejecución

### 🔧 Requisitos previos

* Python ≥ 3.11
* PostgreSQL ≥ 15
* (Opcional) Docker y Docker Compose

### ▶️ Ejecución local

1. **Clonar el repositorio**

   ```bash
   git clone https://github.com/AnteroEscuder/NutriraceBackend
   cd NutriraceBackend
   ```

2. **Crear entorno virtual e instalar dependencias**

   ```bash
   python -m venv venv
   source venv/bin/activate   # En Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configurar variables de entorno**
   Crea un archivo `.env` en la raíz del proyecto con este contenido:

   ```bash
   DATABASE_URL=postgresql+psycopg2://nutribase:nutripass@localhost:5432/nutridb
   JWT_SECRET=cambiar_este_secret
   CORS_ORIGINS=http://localhost:5173
   ```

4. **Iniciar el servidor**

   ```bash
   uvicorn app.main:app --reload
   ```

5. **Abrir la documentación interactiva**
   👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Pruebas automatizadas

```bash
pytest -v
```

> Incluye pruebas para autenticación, creación de usuarios, endpoints y validaciones de datos.

---

## 🐳 Despliegue con Docker

Para levantar el entorno completo (backend + base de datos) con Docker Compose:

```bash
docker compose up --build
```

### Estructura del `docker-compose.yml` (resumen)

```yaml
version: "3.9"
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_USER: nutribase
      POSTGRES_PASSWORD: nutripass
      POSTGRES_DB: nutridb
    ports:
      - "5432:5432"
    volumes:
      - db_data:/var/lib/postgresql/data

  backend:
    build: .
    environment:
      DATABASE_URL: postgresql+psycopg2://nutribase:nutripass@db:5432/nutridb
      JWT_SECRET: cambiar_este_secret
      CORS_ORIGINS: http://localhost:5173
    depends_on:
      - db
    ports:
      - "8000:8000"
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000

volumes:
  db_data:
```

---

## 📦 Endpoints principales

| Método                | Ruta                              | Descripción |
| --------------------- | --------------------------------- | ----------- |
| `POST /auth/register` | Registro de usuario               |             |
| `POST /auth/login`    | Login y generación de token JWT   |             |
| `GET /foods`          | Buscar alimentos                  |             |
| `GET /foods/{id}`     | Consultar alimento por ID         |             |
| `POST /meals`         | Registrar comida del usuario      |             |
| `GET /meals`          | Listar comidas por fecha          |             |
| `GET /goals`          | Consultar objetivos nutricionales |             |
| `PUT /goals`          | Actualizar objetivos              |             |

---

## 🔒 Seguridad y validaciones

* Hash de contraseñas con **bcrypt**
* Tokens **JWT** con expiración configurable
* CORS configurado según entorno
* Validaciones con **Pydantic**
* Control de acceso a endpoints protegidos

---

## 🧱 Integración con frontend

Este backend está diseñado para integrarse con el siguiente repositorio:

🔗 [NutriTrace Frontend](https://github.com/AnteroEscuder/NutritraceFrontend)

---

## 👩‍💻 Autor

* **Antero José Escuder Omenat** — Desarrollo y documentación
* **Tutor:** Jorge Agustín Barón Abad — IES Polígono Sur

---

> 📘 Proyecto desarrollado como parte del **Hito 1: Entrega de Arquitectura de Proyecto v0.1**, dentro del módulo de *Tecnologías Web y Entornos de Desarrollo*.