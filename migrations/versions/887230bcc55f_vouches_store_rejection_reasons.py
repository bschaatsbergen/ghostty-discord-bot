"""Vouches store rejection reasons

Revision ID: 887230bcc55f
Revises: f66337b3b44b
Create Date: 2024-10-02 20:49:36.499970+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "887230bcc55f"
down_revision: Union[str, None] = "f66337b3b44b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("vouches", sa.Column("reason", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("vouches", "reason")
    # ### end Alembic commands ###
