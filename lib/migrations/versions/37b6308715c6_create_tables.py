"""Create Tables

Revision ID: 37b6308715c6
Revises: f454484ab89f
Create Date: 2023-12-13 07:45:22.420041

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37b6308715c6'
down_revision = 'f454484ab89f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('people',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('first_name', sa.String(), nullable=True),
        sa.Column('last_name', sa.String(), nullable=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('user_relashionship', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('relationships',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('type_of_relationship', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('first_name', sa.String(), nullable=True),
        sa.Column('last_name', sa.String(), nullable=True),
        sa.Column('user_relashionship', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('connections',
        sa.Column('individual1_id', sa.Integer(), sa.ForeignKey('people.id'), nullable=False),
        sa.Column('individual2_id', sa.Integer(), sa.ForeignKey('people.id'), nullable=False),
        sa.Column('relationship_id', sa.Integer(), sa.ForeignKey('relationships.id'), nullable=False),
        sa.Column('users_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.PrimaryKeyConstraint('relationship_id', 'users_id')
    )

def downgrade():
    op.drop_table('connections')
    op.drop_table('users')
    op.drop_table('relationships')
    op.drop_table('people')
