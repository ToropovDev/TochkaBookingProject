"""add level

Revision ID: 5b29427dda60
Revises: 659598133d11
Create Date: 2024-05-08 23:46:13.124291

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b29427dda60'
down_revision: Union[str, None] = 'd2781f133458'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('game_level',
    sa.Column('code', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('code')
    )
    op.add_column('game', sa.Column('level', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'game', 'game_level', ['level'], ['code'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'game', type_='foreignkey')
    op.drop_column('game', 'level')
    op.drop_table('game_level')
    # ### end Alembic commands ###
