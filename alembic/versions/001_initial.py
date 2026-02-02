"""initial migration

Revision ID: 001_initial
Revises: 
Create Date: 2026-01-31 12:30:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as pg


revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # using plain string for order status to avoid DB enum creation issues
    # (application still uses OrderStatus enum for logic)

    # products table
    op.create_table(
        'products',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('sku', sa.String(length=64), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('image_url', sa.String(length=1024), nullable=True),
        sa.Column('category', sa.String(length=128), nullable=True),
    )
    op.create_index(op.f('ix_products_sku'), 'products', ['sku'], unique=True)

    # orders table
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('customer_name', sa.String(length=255), nullable=False),
        sa.Column('customer_email', sa.String(length=255), nullable=False),
        sa.Column('items', pg.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('total_amount', sa.Float(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='pending'),
        sa.Column('payment_id', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('orders')
    op.drop_index(op.f('ix_products_sku'), table_name='products')
    op.drop_table('products')
    op.execute("DROP TYPE IF EXISTS orderstatus;")
