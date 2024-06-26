"""edit payment

Revision ID: 068eefe54031
Revises: 528630fe8d3d
Create Date: 2024-06-06 16:08:29.691391

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '068eefe54031'
down_revision: Union[str, None] = '528630fe8d3d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('payment', sa.Column('game_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'payment', 'game', ['game_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'payment', type_='foreignkey')
    op.drop_column('payment', 'game_id')
    # ### end Alembic commands ###
