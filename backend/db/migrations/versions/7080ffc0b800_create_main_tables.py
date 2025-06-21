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
 
 
def create_bot_users_table() -> None:
    op.create_table(
        "bot_users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.Text, nullable=False, index=True),
        sa.Column("login_date", sa.Date, nullable=False, index=True),
        sa.Column("login_time", sa.Time, nullable=False, index=True),
        sa.Column(";ast_used_date", sa.Date, nullable=False, index=True),
        sa.Column("last_used_time", sa.Time, nullable=False, index=True)
    )
 
 
def upgrade() -> None:
    create_bot_users_table()
 
 
def downgrade() -> None:
    op.drop_table("bot_users")
 
 