# Crear migracion cada vez
> alembic revision --autogenerate -m "initial tables"

# Ejecutar SQL generado y aplicar tras cada migracion
> alembic upgrade head