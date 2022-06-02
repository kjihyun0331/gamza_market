"""empty message

Revision ID: 0532d529770a
Revises: 3d2bcd064645
Create Date: 2022-05-30 20:29:07.709122

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0532d529770a'
down_revision = '3d2bcd064645'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('student', sa.Column('id', sa.Integer(), autoincrement=True, nullable=False))
    op.create_unique_constraint(None, 'student', ['id'])
    op.drop_column('student', 'student_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('student', sa.Column('student_id', sa.INTEGER(), nullable=False))
    op.drop_constraint(None, 'student', type_='unique')
    op.drop_column('student', 'id')
    # ### end Alembic commands ###