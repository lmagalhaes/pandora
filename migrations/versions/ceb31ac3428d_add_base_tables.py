"""add base tables

Revision ID: ceb31ac3428d
Revises: 
Create Date: 2020-09-09 19:04:52.552722

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy_utils.types import EmailType, ScalarListType


# revision identifiers, used by Alembic.
revision = 'ceb31ac3428d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('company',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('food',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=15), nullable=False),
    sa.Column('is_fruit', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('person',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('has_died', sa.Boolean(), nullable=True),
    sa.Column('eye_color', sa.String(length=32), nullable=True),
    sa.Column('email', EmailType(length=255), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('address', sa.String(length=255), nullable=True),
    sa.Column('tags', ScalarListType(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('company_employs_person',
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('person_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ),
    sa.ForeignKeyConstraint(['person_id'], ['person.id'], ),
    sa.PrimaryKeyConstraint('company_id', 'person_id')
    )
    op.create_table('person_likes_food',
    sa.Column('person_id', sa.Integer(), nullable=False),
    sa.Column('food_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['food_id'], ['food.id'], ),
    sa.ForeignKeyConstraint(['person_id'], ['person.id'], ),
    sa.PrimaryKeyConstraint('person_id', 'food_id')
    )
    op.create_table('person_relates_to_person',
    sa.Column('person_id', sa.Integer(), nullable=False),
    sa.Column('friend_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['friend_id'], ['person.id'], ),
    sa.ForeignKeyConstraint(['person_id'], ['person.id'], ),
    sa.PrimaryKeyConstraint('person_id', 'friend_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('person_relates_to_person')
    op.drop_table('person_likes_food')
    op.drop_table('company_employs_person')
    op.drop_table('person')
    op.drop_table('food')
    op.drop_table('company')
    # ### end Alembic commands ###
