"""add_image_url_to_messages

Revision ID: 6f0be8497fd4
Revises: 7a0c6638676c
Create Date: 2025-12-17 00:49:46.149526

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6f0be8497fd4'
down_revision: Union[str, Sequence[str], None] = '7a0c6638676c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 添加 image_url 字段到 private_messages 表
    op.add_column('private_messages', 
        sa.Column('image_url', sa.String(length=500), nullable=True))
    
    # 添加 image_url 字段到 random_chat_history 表
    op.add_column('random_chat_history',
        sa.Column('image_url', sa.String(length=500), nullable=True))
    
    # 修改 message_text 为可空（支持纯图片消息）
    # SQLite 不支持直接修改列，需要使用 batch 模式
    with op.batch_alter_table('private_messages') as batch_op:
        batch_op.alter_column('message_text', nullable=True)
    
    with op.batch_alter_table('random_chat_history') as batch_op:
        batch_op.alter_column('message_text', nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('random_chat_history', 'image_url')
    op.drop_column('private_messages', 'image_url')
    
    # 恢复 message_text 为非空
    with op.batch_alter_table('private_messages') as batch_op:
        batch_op.alter_column('message_text', nullable=False)
    
    with op.batch_alter_table('random_chat_history') as batch_op:
        batch_op.alter_column('message_text', nullable=False)
