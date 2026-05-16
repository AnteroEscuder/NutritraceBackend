"""add system foods

Revision ID: 2b8f0c9a1d6e
Revises: b26fde15d14a
Create Date: 2026-05-16 12:35:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "2b8f0c9a1d6e"
down_revision: Union[str, Sequence[str], None] = "b26fde15d14a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


SYSTEM_FOODS = [
    {"name": "Arroz blanco cocido", "calories": 130.0, "protein": 2.7, "carbs": 28.0, "fat": 0.3},
    {"name": "Pechuga de pollo", "calories": 165.0, "protein": 31.0, "carbs": 0.0, "fat": 3.6},
    {"name": "Avena", "calories": 389.0, "protein": 16.9, "carbs": 66.3, "fat": 6.9},
    {"name": "Huevo", "calories": 155.0, "protein": 13.0, "carbs": 1.1, "fat": 11.0},
    {"name": "Manzana", "calories": 52.0, "protein": 0.3, "carbs": 14.0, "fat": 0.2},
    {"name": "Platano", "calories": 89.0, "protein": 1.1, "carbs": 22.8, "fat": 0.3},
    {"name": "Yogur natural", "calories": 61.0, "protein": 3.5, "carbs": 4.7, "fat": 3.3},
    {"name": "Aceite de oliva", "calories": 884.0, "protein": 0.0, "carbs": 0.0, "fat": 100.0},
    {"name": "Pan integral", "calories": 247.0, "protein": 13.0, "carbs": 41.0, "fat": 4.2},
    {"name": "Lentejas cocidas", "calories": 116.0, "protein": 9.0, "carbs": 20.0, "fat": 0.4},
]


def upgrade() -> None:
    op.add_column("foods", sa.Column("is_system", sa.Boolean(), server_default=sa.false(), nullable=False))
    op.alter_column("foods", "user_id", existing_type=sa.Integer(), nullable=True)

    foods_table = sa.table(
        "foods",
        sa.column("name", sa.String()),
        sa.column("calories", sa.Float()),
        sa.column("protein", sa.Float()),
        sa.column("carbs", sa.Float()),
        sa.column("fat", sa.Float()),
        sa.column("user_id", sa.Integer()),
        sa.column("is_system", sa.Boolean()),
    )

    op.bulk_insert(
        foods_table,
        [{**food, "user_id": None, "is_system": True} for food in SYSTEM_FOODS],
    )


def downgrade() -> None:
    quoted_names = ", ".join(f"'{food['name']}'" for food in SYSTEM_FOODS)
    op.execute(f"DELETE FROM foods WHERE is_system = true AND name IN ({quoted_names})")
    op.alter_column("foods", "user_id", existing_type=sa.Integer(), nullable=False)
    op.drop_column("foods", "is_system")
