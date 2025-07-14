"""create_main_tables
 
Revision ID: 7080ffc0b800
Revises: 
Create Date: 2025-06-21 17:44:14.455351
 
"""
from alembic import op
import sqlalchemy as sa

 
# revision identifiers, used by Alembic
revision = '7080ffc0b800'
down_revision = None
branch_labels = None
depends_on = None
 
def create_users_table() -> None:
    op.create_table(
        "users",
        sa.Column("user_id", sa.Integer, primary_key=True),
        sa.Column("alias", sa.Text, nullable=False, index=True),
        sa.Column("mail", sa.Text, nullable=True, index=True, server_default=None),
        sa.Column("name", sa.Text, nullable=True, index=True, server_default=None),
        sa.Column("surname", sa.Text, nullable=True, index=True, server_default=None),
        sa.Column("patronymic", sa.Text, nullable=True, index=True, server_default=None),
        sa.Column("phone_number", sa.Text, nullable=True, index=True, server_default=None),
        sa.Column("citizens", sa.Text, nullable=True, index=True, server_default=None),
        sa.Column("duty_to_work", sa.Text, nullable=True, index=True, server_default=None),
        sa.Column("duty_status", sa.Text, nullable=True, index=True, server_default=None),
        sa.Column("grant_amount", sa.Integer, nullable=True, index=True, server_default=None),
        sa.Column("duty_period", sa.Integer, nullable=True, index=True, server_default=None),
        sa.Column("company", sa.Text, nullable=True, index=True, server_default=None),
        sa.Column("position", sa.Text, nullable=True, index=True, server_default=None),
        sa.Column("start_date", sa.Date, nullable=True, index=True, server_default=None),
        sa.Column("end_date", sa.Date, nullable=True, index=True, server_default=None),
        sa.Column("salary", sa.Integer, nullable=True, index=True, server_default=None),
    )

# sa.Column("cleaning_type", sa.Text, nullable=False, server_default="spot_clean"),

def upgrade() -> None:
    create_users_table()
 
 
def downgrade() -> None:
    op.drop_table("users")
 
 