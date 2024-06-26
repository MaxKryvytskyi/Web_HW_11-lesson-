"""init

Revision ID: c0111173314d
Revises: 286cd6eaf04a
Create Date: 2024-03-24 03:27:12.414489

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c0111173314d'
down_revision: Union[str, None] = '286cd6eaf04a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contacts', sa.Column('first_name', sa.String(length=40), nullable=False))
    op.add_column('contacts', sa.Column('last_name', sa.String(length=40), nullable=False))
    op.alter_column('contacts', 'phone',
               existing_type=sa.VARCHAR(length=15),
               type_=sa.String(length=13),
               existing_nullable=False)
    op.alter_column('contacts', 'birthday',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.DATE(),
               existing_nullable=True)
    op.drop_column('contacts', 'lastname')
    op.drop_column('contacts', 'name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contacts', sa.Column('name', sa.VARCHAR(length=40), autoincrement=False, nullable=False))
    op.add_column('contacts', sa.Column('lastname', sa.VARCHAR(length=40), autoincrement=False, nullable=False))
    op.alter_column('contacts', 'birthday',
               existing_type=sa.DATE(),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=True)
    op.alter_column('contacts', 'phone',
               existing_type=sa.String(length=13),
               type_=sa.VARCHAR(length=15),
               existing_nullable=False)
    op.drop_column('contacts', 'last_name')
    op.drop_column('contacts', 'first_name')
    # ### end Alembic commands ###
