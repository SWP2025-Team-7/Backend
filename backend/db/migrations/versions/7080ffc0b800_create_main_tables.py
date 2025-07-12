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
        sa.Column("id", sa.Integer,  primary_key=True),
        sa.Column("user_id", sa.Integer,nullable=False, index=True,),
        sa.Column("username", sa.Text, nullable=False, index=True),
        sa.Column("login_date", sa.Date, nullable=False, index=True),
        sa.Column("login_time", sa.Time, nullable=False, index=True),
        sa.Column("last_used_date", sa.Date, nullable=False, index=True),
        sa.Column("last_used_time", sa.Time, nullable=False, index=True)
    )
 
def create_users_table() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, nullable=False, index=True),
        sa.Column("alias", sa.Text, nullable=False, index=True),
        sa.Column("mail", sa.Text, nullable=False, index=True),
        sa.Column("name", sa.Text, nullable=False, index=True),
        sa.Column("surname", sa.Text, nullable=False, index=True),
        sa.Column("patronymic", sa.Text, nullable=False, index=True),
        sa.Column("phone_number", sa.Text, nullable=True, index=True),
        sa.Column("citizens", sa.Text, nullable=True, index=True),
        sa.Column("duty_to_work", sa.Text, nullable=True, index=True, server_default="yes"),
        sa.Column("duty_status", sa.Text, nullable=True, index=True, server_default="do_not_get_in_touch"),
        sa.Column("grant_amount", sa.Integer, nullable=True, index=True),
        sa.Column("duty_period", sa.Integer, nullable=True, index=True),
        sa.Column("company", sa.Text, nullable=True, index=True),
        sa.Column("resume_path", sa.Text, nullable=True, index=True),
        sa.Column("position", sa.Text, nullable=True, index=True),
        sa.Column("start_date", sa.Date, nullable=True, index=True),
        sa.Column("end_date", sa.Date, nullable=True, index=True),
        sa.Column("salary", sa.Integer, nullable=True, index=True),
        sa.Column("working_reference_path", sa.Text, nullable=True, index=True),
        sa.Column("ndfl1_path", sa.Text, nullable=True, index=True),
        sa.Column("ndfl2_path", sa.Text, nullable=True, index=True),
        sa.Column("ndfl3_path", sa.Text, nullable=True, index=True),
        sa.Column("ndfl4_path", sa.Text, nullable=True, index=True)
    )
    
# sa.Column("cleaning_type", sa.Text, nullable=False, server_default="spot_clean"),

def upgrade() -> None:
    create_bot_users_table()
    create_users_table()
 
 
def downgrade() -> None:
    op.drop_table("bot_users")
    op.drop_table("users")
 
 