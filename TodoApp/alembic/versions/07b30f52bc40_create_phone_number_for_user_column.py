"""Create phone number for user column

Revision ID: 07b30f52bc40
Revises: 
Create Date: 2025-10-01 15:53:36.060824

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '07b30f52bc40'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('user',sa.Column('phone_number',sa.String(),nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("user","phone_number")
