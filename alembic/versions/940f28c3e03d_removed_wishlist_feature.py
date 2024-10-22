"""Removed Wishlist feature

Revision ID: 940f28c3e03d
Revises: ba11e54c43f2
Create Date: 2024-06-25 19:03:05.562948

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '940f28c3e03d'
down_revision: Union[str, None] = 'ba11e54c43f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_wishlist_id', table_name='wishlist')
    op.drop_table('wishlist')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('wishlist',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('product_id', sa.INTEGER(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_wishlist_id', 'wishlist', ['id'], unique=False)
    # ### end Alembic commands ###
