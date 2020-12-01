"""empty message

Revision ID: 74c9b2785972
Revises: 
Create Date: 2020-11-30 16:49:23.795756

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '74c9b2785972'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('colors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hex', sa.String(length=7), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('mode', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('hex'),
    sa.UniqueConstraint('name')
    )
    op.create_table('stamps',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('stamp', sa.String(length=50), nullable=False),
    sa.Column('type', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('stamp')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('color_id', sa.Integer(), nullable=True),
    sa.Column('stamp_id', sa.Integer(), nullable=False),
    sa.Column('birthday', sa.Date(), nullable=True),
    sa.Column('hashed_password', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['color_id'], ['colors.id'], ),
    sa.ForeignKeyConstraint(['stamp_id'], ['stamps.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('bonds',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user1_id', sa.Integer(), nullable=False),
    sa.Column('user2_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user1_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user2_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('programs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('program', sa.String(length=50), nullable=False),
    sa.Column('description', sa.String(length=250), nullable=True),
    sa.Column('color_id', sa.Integer(), nullable=True),
    sa.Column('stamp_id', sa.Integer(), nullable=False),
    sa.Column('creator_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['color_id'], ['colors.id'], ),
    sa.ForeignKeyConstraint(['creator_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['stamp_id'], ['stamps.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('habits',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('habit', sa.String(length=50), nullable=False),
    sa.Column('description', sa.String(length=250), nullable=True),
    sa.Column('frequency', sa.String(length=7), nullable=False),
    sa.Column('color_id', sa.Integer(), nullable=True),
    sa.Column('stamp_id', sa.Integer(), nullable=False),
    sa.Column('program_id', sa.Integer(), nullable=True),
    sa.Column('creator_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['color_id'], ['colors.id'], ),
    sa.ForeignKeyConstraint(['creator_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['program_id'], ['programs.id'], ),
    sa.ForeignKeyConstraint(['stamp_id'], ['stamps.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('members',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('program_id', sa.Integer(), nullable=False),
    sa.Column('member_id', sa.Integer(), nullable=False),
    sa.Column('stamper_id', sa.Integer(), nullable=True),
    sa.Column('points', sa.Integer(), nullable=False),
    sa.Column('joined_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['member_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['program_id'], ['programs.id'], ),
    sa.ForeignKeyConstraint(['stamper_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rewards',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=50), nullable=False),
    sa.Column('reward', sa.String(length=50), nullable=False),
    sa.Column('description', sa.String(length=250), nullable=True),
    sa.Column('cost', sa.Integer(), nullable=False),
    sa.Column('color_id', sa.Integer(), nullable=True),
    sa.Column('limit_per_member', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('stamp_id', sa.Integer(), nullable=False),
    sa.Column('program_id', sa.Integer(), nullable=True),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['color_id'], ['colors.id'], ),
    sa.ForeignKeyConstraint(['creator_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['program_id'], ['programs.id'], ),
    sa.ForeignKeyConstraint(['stamp_id'], ['stamps.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('daily_stamps',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('status', sa.Enum('unstamped', 'pending', 'stamped', name='status'), nullable=True),
    sa.Column('habit_id', sa.Integer(), nullable=False),
    sa.Column('member_id', sa.Integer(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['habit_id'], ['habits.id'], ),
    sa.ForeignKeyConstraint(['member_id'], ['members.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('redeemed',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('reward_id', sa.Integer(), nullable=False),
    sa.Column('redeemed_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['reward_id'], ['rewards.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('redeemed')
    op.drop_table('daily_stamps')
    op.drop_table('rewards')
    op.drop_table('members')
    op.drop_table('habits')
    op.drop_table('programs')
    op.drop_table('bonds')
    op.drop_table('users')
    op.drop_table('stamps')
    op.drop_table('colors')
    # ### end Alembic commands ###
