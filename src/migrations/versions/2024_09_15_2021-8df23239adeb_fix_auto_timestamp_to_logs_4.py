"""Fix auto timestamp to logs 4

Revision ID: 8df23239adeb
Revises: 5f48f88e4f64
Create Date: 2024-09-15 20:21:09.245321

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8df23239adeb'
down_revision: Union[str, None] = '5f48f88e4f64'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###