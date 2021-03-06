"""Everthing to host an event where attendees can accept and decline.

Revision ID: b668bbf2d11a
Revises: 
Create Date: 2020-05-14 00:58:06.549211

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b668bbf2d11a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('duration', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('attendee',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nick', sa.String(length=128), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('proposal',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('appointment', sa.DateTime(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('frees',
    sa.Column('attendee_id', sa.Integer(), nullable=False),
    sa.Column('proposal_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['attendee_id'], ['attendee.id'], ),
    sa.ForeignKeyConstraint(['proposal_id'], ['proposal.id'], ),
    sa.PrimaryKeyConstraint('attendee_id', 'proposal_id')
    )
    op.create_table('occupides',
    sa.Column('attendee_id', sa.Integer(), nullable=False),
    sa.Column('proposal_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['attendee_id'], ['attendee.id'], ),
    sa.ForeignKeyConstraint(['proposal_id'], ['proposal.id'], ),
    sa.PrimaryKeyConstraint('attendee_id', 'proposal_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('occupides')
    op.drop_table('frees')
    op.drop_table('proposal')
    op.drop_table('attendee')
    op.drop_table('event')
    # ### end Alembic commands ###
