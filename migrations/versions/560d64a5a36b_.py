"""empty message

Revision ID: 560d64a5a36b
Revises: ac4d19841522
Create Date: 2023-03-17 08:05:53.664575

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '560d64a5a36b'
down_revision = 'ac4d19841522'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('character',
    sa.Column('idx', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(length=20), nullable=True),
    sa.Column('scenario_title', sa.String(length=100), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('content', sa.String(length=500), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('is_opened', sa.Boolean(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['scenario_title'], ['scenario.title'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('idx')
    )
    op.create_table('element',
    sa.Column('idx', sa.Integer(), nullable=False),
    sa.Column('character_name', sa.String(length=50), nullable=True),
    sa.Column('element', sa.String(length=100), nullable=False),
    sa.Column('content', sa.String(length=1000), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('is_opened', sa.Boolean(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['character_name'], ['character.name'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('idx')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('element')
    op.drop_table('character')
    # ### end Alembic commands ###
