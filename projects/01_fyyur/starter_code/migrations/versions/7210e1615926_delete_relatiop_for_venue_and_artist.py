"""delete relatiop for venue and artist

Revision ID: 7210e1615926
Revises: 4d16d8dfb567
Create Date: 2020-05-13 19:08:33.277755

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7210e1615926'
down_revision = '4d16d8dfb567'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('Venue_artist_id_fkey', 'Venue', type_='foreignkey')
    op.drop_column('Venue', 'artist_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('artist_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('Venue_artist_id_fkey', 'Venue', 'Artist', ['artist_id'], ['id'])
    # ### end Alembic commands ###
