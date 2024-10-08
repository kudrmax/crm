"""Fix contact_id in MLog

Revision ID: f13d50101759
Revises: 09102b64f5d1
Create Date: 2024-09-07 19:05:09.471358

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f13d50101759'
down_revision: Union[str, None] = '09102b64f5d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('logs', sa.Column('contact_id', sa.UUID(), nullable=False))
    op.create_foreign_key(None, 'logs', 'contacts', ['contact_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'logs', type_='foreignkey')
    op.drop_column('logs', 'contact_id')
    # ### end Alembic commands ###
