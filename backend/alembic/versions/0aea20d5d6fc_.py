"""empty message

Revision ID: 0aea20d5d6fc
Revises: 8fd205c94190
Create Date: 2019-01-26 22:49:05.784040

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0aea20d5d6fc'
down_revision = '8fd205c94190'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('locations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('mode', sa.Integer(), nullable=True),
    sa.Column('acousticness', sa.Float(), nullable=True),
    sa.Column('danceability', sa.Float(), nullable=True),
    sa.Column('energy', sa.Float(), nullable=True),
    sa.Column('instrumentalness', sa.Float(), nullable=True),
    sa.Column('liveness', sa.Float(), nullable=True),
    sa.Column('loudness', sa.Float(), nullable=True),
    sa.Column('speechiness', sa.Float(), nullable=True),
    sa.Column('valence', sa.Float(), nullable=True),
    sa.Column('tempo', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('songs',
    sa.Column('tunes_id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('spotify_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('mode', sa.Integer(), nullable=True),
    sa.Column('acousticness', sa.Float(), nullable=True),
    sa.Column('danceability', sa.Float(), nullable=True),
    sa.Column('energy', sa.Float(), nullable=True),
    sa.Column('instrumentalness', sa.Float(), nullable=True),
    sa.Column('liveness', sa.Float(), nullable=True),
    sa.Column('loudness', sa.Float(), nullable=True),
    sa.Column('speechiness', sa.Float(), nullable=True),
    sa.Column('valence', sa.Float(), nullable=True),
    sa.Column('tempo', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['artists.id'], ),
    sa.PrimaryKeyConstraint('tunes_id')
    )
    op.create_table('plays',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('location_id', sa.Integer(), nullable=False),
    sa.Column('song_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ),
    sa.ForeignKeyConstraint(['song_id'], ['songs.tunes_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('plays')
    op.drop_table('songs')
    op.drop_table('locations')
    op.drop_table('artists')
    # ### end Alembic commands ###
