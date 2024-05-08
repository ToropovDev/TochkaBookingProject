"""add game creator

Revision ID: f3d5656fd85c
Revises: c22f27b2974f
Create Date: 2024-05-08 23:57:29.414232

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3d5656fd85c'
down_revision: Union[str, None] = 'c22f27b2974f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('game', sa.Column('creator', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'game', 'user', ['creator'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'game', type_='foreignkey')
    op.drop_column('game', 'creator')
    # ### end Alembic commands ###