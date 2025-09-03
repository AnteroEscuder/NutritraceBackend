### 🟡 Paso 1 – Cálculo nutricional por comida y por día

Cuando un usuario registra una comida:

* Calcular calorías totales de esa comida:
  `total = (food.calories * quantity) / 100`
* Igual para proteínas, carbohidratos y grasas.

→ También podríamos hacer un resumen diario por usuario:

```json
{
  "user_id": 1,
  "date": "2025-09-01",
  "total_calories": 1320,
  "protein": 85.3,
  "carbs": 160.4,
  "fat": 45.7
}
```

---

### 🟡 Paso 2 – Autenticación (registro/login con JWT)

Ahora los usuarios se crean sin contraseña y cualquiera puede usar la API.
✅ Lo ideal:

* Añadir campos `password_hash` en el modelo `User`
* Crear `/register`, `/login` y `/me` protegidas por token
* Usar JWT con `fastapi.security`

---

### 🟡 Paso 3 – Filtros en los endpoints

* `/meals?user_id=1&date=2025-09-01`
* `/foods?name=pollo`
* `/users/1/meals`

Esto permite crear un dashboard o app que filtre datos fácilmente.

---

### 🟡 Paso 4 – Migraciones con Alembic

Ahora creas tablas con `create_tables.py`, pero lo ideal es:

* Instalar y configurar **Alembic**
* Versionar cambios en la base de datos
* Generar migraciones automáticas cuando cambies los modelos

---

### 🟢 Paso 5 – Frontend o cliente externo

