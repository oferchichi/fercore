"""empty message

Revision ID: 1d428415a99f
Revises: 33f95e7de988
Create Date: 2019-03-10 14:17:23.195642

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d428415a99f'
down_revision = '33f95e7de988'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('apptype',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('avability',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('environnement',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('gtmip',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('wide_ip', sa.String(length=80), nullable=False),
    sa.Column('pub_antares', sa.String(length=80), nullable=True),
    sa.Column('pub_alberio', sa.String(length=80), nullable=True),
    sa.Column('dpub_alb', sa.String(length=80), nullable=True),
    sa.Column('dpub_ant', sa.String(length=80), nullable=True),
    sa.Column('dpriv_ant', sa.String(length=80), nullable=True),
    sa.Column('dpriv2_ant', sa.String(length=80), nullable=True),
    sa.Column('dpriv_alb', sa.String(length=80), nullable=True),
    sa.Column('dpriv2_alb', sa.String(length=80), nullable=True),
    sa.Column('reserverd_on', sa.DateTime(), nullable=False),
    sa.Column('reserverd_par', sa.String(length=80), nullable=True),
    sa.Column('nomapp', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nomapp'),
    sa.UniqueConstraint('wide_ip')
    )
    op.create_table('portStandardInternet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('ports',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('used', sa.String(length=80), nullable=False),
    sa.Column('type_port', sa.String(length=80), nullable=False),
    sa.Column('nomapp', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sysUptime',
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('lastCheck', sa.String(length=100), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('acknowledge', sa.Integer(), nullable=True),
    sa.Column('comment', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_table('systeminformation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('trigram',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('application',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nomapp', sa.String(length=80), nullable=False),
    sa.Column('status', sa.String(length=80), nullable=False),
    sa.Column('fqdn', sa.String(length=80), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=False),
    sa.Column('createur', sa.String(length=200), nullable=False),
    sa.Column('pub_date', sa.DateTime(), nullable=False),
    sa.Column('systeminformation', sa.Integer(), nullable=False),
    sa.Column('trigram', sa.Integer(), nullable=False),
    sa.Column('apptype', sa.Integer(), nullable=False),
    sa.Column('environnement', sa.Integer(), nullable=False),
    sa.Column('avability', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['apptype'], ['apptype.id'], ),
    sa.ForeignKeyConstraint(['avability'], ['avability.id'], ),
    sa.ForeignKeyConstraint(['environnement'], ['environnement.id'], ),
    sa.ForeignKeyConstraint(['systeminformation'], ['systeminformation.id'], ),
    sa.ForeignKeyConstraint(['trigram'], ['trigram.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nomapp')
    )
    op.create_table('equipement',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('ip', sa.String(length=80), nullable=False),
    sa.Column('port', sa.String(length=20), nullable=True),
    sa.Column('login', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.Column('type_equipement', sa.String(length=80), nullable=False),
    sa.Column('fonction', sa.String(length=80), nullable=False),
    sa.Column('envi', sa.String(length=80), nullable=True),
    sa.Column('datacenter', sa.String(length=80), nullable=True),
    sa.Column('clusterName', sa.String(length=80), nullable=True),
    sa.Column('system_info', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['system_info'], ['systeminformation.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reverseproxy',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('qualification', sa.String(length=80), nullable=True),
    sa.Column('uidReverseProxy', sa.String(length=200), nullable=False),
    sa.Column('uidInterface', sa.String(length=200), nullable=False),
    sa.Column('ip', sa.String(length=80), nullable=False),
    sa.Column('rp_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['rp_id'], ['equipement.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tunnel',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('reverseproxy', sa.String(length=200), nullable=False),
    sa.Column('interface_incomming', sa.String(length=200), nullable=False),
    sa.Column('interface_outcomming', sa.String(length=200), nullable=False),
    sa.Column('portEntrer', sa.String(length=80), nullable=False),
    sa.Column('portSortie', sa.String(length=80), nullable=False),
    sa.Column('rp_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['rp_id'], ['equipement.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('virtualserver',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('portService', sa.String(length=80), nullable=False),
    sa.Column('description', sa.String(length=80), nullable=False),
    sa.Column('sourceAddresstranslation', sa.String(length=80), nullable=False),
    sa.Column('snatPool', sa.String(length=80), nullable=False),
    sa.Column('ipvip', sa.String(length=80), nullable=False),
    sa.Column('fullpath', sa.String(length=80), nullable=False),
    sa.Column('partition', sa.String(length=80), nullable=False),
    sa.Column('app_id', sa.Integer(), nullable=False),
    sa.Column('equipement_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['app_id'], ['application.id'], ),
    sa.ForeignKeyConstraint(['equipement_id'], ['equipement.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pools',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('partition', sa.String(length=80), nullable=True),
    sa.Column('portService', sa.String(length=80), nullable=True),
    sa.Column('fullpath', sa.String(length=80), nullable=True),
    sa.Column('vs_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['vs_id'], ['virtualserver.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('nodes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('ip', sa.String(length=80), nullable=True),
    sa.Column('fullname', sa.String(length=80), nullable=True),
    sa.Column('partition', sa.String(length=80), nullable=True),
    sa.Column('pool_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['pool_id'], ['pools.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('nodes')
    op.drop_table('pools')
    op.drop_table('virtualserver')
    op.drop_table('tunnel')
    op.drop_table('reverseproxy')
    op.drop_table('equipement')
    op.drop_table('application')
    op.drop_table('trigram')
    op.drop_table('systeminformation')
    op.drop_table('sysUptime')
    op.drop_table('ports')
    op.drop_table('portStandardInternet')
    op.drop_table('gtmip')
    op.drop_table('environnement')
    op.drop_table('avability')
    op.drop_table('apptype')
    # ### end Alembic commands ###
