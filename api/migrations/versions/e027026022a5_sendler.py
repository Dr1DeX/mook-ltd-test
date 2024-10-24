"""sendler

Revision ID: e027026022a5
Revises: fa77621b9894
Create Date: 2024-10-24 22:36:15.866152

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e027026022a5'
down_revision: Union[str, None] = 'fa77621b9894'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('Messages_recipient_id_fkey', 'Messages', type_='foreignkey')
    op.drop_column('Messages', 'recipient_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Messages', sa.Column('recipient_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('Messages_recipient_id_fkey', 'Messages', 'UserProfile', ['recipient_id'], ['id'])
    # ### end Alembic commands ###
