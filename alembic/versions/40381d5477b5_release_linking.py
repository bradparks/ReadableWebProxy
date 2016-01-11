"""release linking

Revision ID: 40381d5477b5
Revises: a4cb7899f08f
Create Date: 2016-01-10 20:27:36.692715

"""

# revision identifiers, used by Alembic.
revision = '40381d5477b5'
down_revision = 'a4cb7899f08f'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

from sqlalchemy_utils.types import TSVectorType
from sqlalchemy_searchable import make_searchable
import sqlalchemy_utils

# Patch in knowledge of the citext type, so it reflects properly.
from sqlalchemy.dialects.postgresql.base import ischema_names
import citext
import queue
import datetime
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.dialects.postgresql import TSVECTOR
ischema_names['citext'] = citext.CIText



def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('web_pages', sa.Column('previous_release', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'web_pages', 'web_page_history', ['previous_release'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'web_pages', type_='foreignkey')
    op.drop_column('web_pages', 'previous_release')
    ### end Alembic commands ###
