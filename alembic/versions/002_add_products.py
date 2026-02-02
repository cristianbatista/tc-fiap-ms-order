"""no-op migration placeholder

Revision ID: 002_products
Revises: 001_initial
Create Date: 2026-01-31 12:30:00.000001
"""
from alembic import op


revision = '002_products'
down_revision = '001_initial'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # no-op: initial migration contains schema
    pass


def downgrade() -> None:
    pass
