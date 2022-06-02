"""empty message

Revision ID: 3d2bcd064645
Revises: 
Create Date: 2022-05-30 20:27:33.856338

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d2bcd064645'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('students')
    op.add_column('student', sa.Column('id', sa.Integer(), autoincrement=True, nullable=False))
    op.create_unique_constraint(None, 'student', ['id'])
    op.drop_column('student', 'student_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('student', sa.Column('student_id', sa.INTEGER(), nullable=False))
    op.drop_constraint(None, 'student', type_='unique')
    op.drop_column('student', 'id')
    op.create_table('students',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('s_id', sa.VARCHAR(length=30), nullable=True),
    sa.Column('s_name', sa.VARCHAR(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###
