"""initial schema

Revision ID: 2b90aabac5ba
Revises:
Create Date: 2026-05-20 18:32:29.625811

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '2b90aabac5ba'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- users ---
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('password_hash', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username'),
    )

    # --- oauth_accounts ---
    op.create_table(
        'oauth_accounts',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('provider', sa.String(), nullable=False),
        sa.Column('provider_user_id', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('provider', 'provider_user_id'),
    )

    # --- user_settings ---
    op.create_table(
        'user_settings',
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('quiz_length', sa.Integer(), server_default='10', nullable=False),
        sa.Column('romaji_visible', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('sound_enabled', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('theme', sa.String(), server_default="'dark'", nullable=False),
        sa.Column('language', sa.String(), server_default="'en'", nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('user_id'),
    )

    # --- user_progress ---
    op.create_table(
        'user_progress',
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('xp', sa.Integer(), server_default='0', nullable=False),
        sa.Column('streak', sa.Integer(), server_default='0', nullable=False),
        sa.Column('last_played_date', sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('user_id'),
    )

    # --- quiz_history ---
    op.create_table(
        'quiz_history',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('mode', sa.String(), nullable=False),
        sa.Column('score', sa.Integer(), nullable=False),
        sa.Column('total', sa.Integer(), nullable=False),
        sa.Column('xp_gained', sa.Integer(), nullable=False),
        sa.Column('played_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_quiz_history_user_id', 'quiz_history', ['user_id'])

    # --- character_stats ---
    op.create_table(
        'character_stats',
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('char_key', sa.String(), nullable=False),
        sa.Column('correct', sa.Integer(), server_default='0', nullable=False),
        sa.Column('incorrect', sa.Integer(), server_default='0', nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('user_id', 'char_key'),
    )

    # --- flashcard_known ---
    op.create_table(
        'flashcard_known',
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('card_id', sa.String(), nullable=False),
        sa.Column('known', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('user_id', 'card_id'),
    )

    # --- favorites ---
    op.create_table(
        'favorites',
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('item_type', sa.String(), nullable=False),
        sa.Column('item_key', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('user_id', 'item_type', 'item_key'),
    )

    # --- kana ---
    op.create_table(
        'kana',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('kana', sa.String(), nullable=False),
        sa.Column('romaji', sa.String(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('grp', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('kana', 'type'),
    )

    # --- vocabulary ---
    op.create_table(
        'vocabulary',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('expression', sa.String(), nullable=False),
        sa.Column('reading', sa.String(), nullable=False),
        sa.Column('meaning', sa.Text(), nullable=False),
        sa.Column('meaning_pt', sa.Text(), nullable=True),
        sa.Column('jlpt', sa.String(), nullable=False),
        sa.Column('pos', sa.String(), nullable=True),
        sa.Column('category', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('expression', 'reading'),
    )

    # --- kanji ---
    op.create_table(
        'kanji',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('kanji', sa.String(), nullable=False),
        sa.Column('meaning', postgresql.ARRAY(sa.Text()), nullable=False),
        sa.Column('meaning_pt', postgresql.ARRAY(sa.Text()), nullable=True),
        sa.Column('onyomi', postgresql.ARRAY(sa.Text()), nullable=False),
        sa.Column('kunyomi', postgresql.ARRAY(sa.Text()), nullable=False),
        sa.Column('jlpt', sa.String(), nullable=False),
        sa.Column('stroke_count', sa.Integer(), nullable=False),
        sa.Column('examples', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('kanji'),
    )


def downgrade() -> None:
    op.drop_table('kanji')
    op.drop_table('vocabulary')
    op.drop_table('kana')
    op.drop_table('favorites')
    op.drop_table('flashcard_known')
    op.drop_table('character_stats')
    op.drop_index('ix_quiz_history_user_id', table_name='quiz_history')
    op.drop_table('quiz_history')
    op.drop_table('user_progress')
    op.drop_table('user_settings')
    op.drop_table('oauth_accounts')
    op.drop_table('users')
