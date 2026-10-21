"""add full text search to document chunks

Revision ID: 90ae30ccc28b
Revises: 01ef835cc51d
Create Date: 2026-09-02 18:10:01.313377

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '90ae30ccc28b'
down_revision: Union[str, Sequence[str], None] = '01ef835cc51d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('document_chunks', sa.Column('search_vector', postgresql.TSVECTOR(), sa.Computed("to_tsvector('simple', text)", persisted=True), nullable=True))
    op.create_index('ix_document_chunks_search_vector_gin', 'document_chunks', ['search_vector'], unique=False, postgresql_using='gin')


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('ix_document_chunks_search_vector_gin', table_name='document_chunks')
    op.drop_column('document_chunks', 'search_vector')