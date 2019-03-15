"""empty message

Revision ID: e417877a5b00
Revises: 1d428415a99f
Create Date: 2019-03-15 23:41:37.400370

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e417877a5b00'
down_revision = '1d428415a99f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tunnel', sa.Column('app_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'tunnel', 'application', ['app_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tunnel', type_='foreignkey')
    op.drop_column('tunnel', 'app_id')
    # ### end Alembic commands ###
