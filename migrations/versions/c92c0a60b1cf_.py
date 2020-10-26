"""empty message

Revision ID: c92c0a60b1cf
Revises: 
Create Date: 2020-10-26 11:24:20.888093

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c92c0a60b1cf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Actor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('actor', sa.String(), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('awards', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Movie',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('movie', sa.String(), nullable=True),
    sa.Column('genres', sa.String(), nullable=True),
    sa.Column('age_rating', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Movie')
    op.drop_table('Actor')
    # ### end Alembic commands ###