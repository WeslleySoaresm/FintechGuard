
"""add conversations and migrate messages

Revision ID: d84724708017
Revises: 45748d1ec0da
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "d84724708017"
down_revision: Union[str, Sequence[str], None] = "45748d1ec0da"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Cria a tabela de conversas.
    op.create_table(
        "conversations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("ticket_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["ticket_id"], ["tickets.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_conversations_ticket_id",
        "conversations",
        ["ticket_id"],
    )
    op.create_index(
        "ix_conversations_user_id",
        "conversations",
        ["user_id"],
    )

    # 2. Adiciona conversation_id temporariamente como opcional.
    op.add_column(
        "conversation_messages",
        sa.Column("conversation_id", sa.Integer(), nullable=True),
    )

    # 3. Cria uma conversa para cada ticket que possui mensagens.
    connection = op.get_bind()

    connection.execute(
        sa.text("""
            INSERT INTO conversations (user_id, ticket_id, created_at)
            SELECT
                tickets.user_id,
                tickets.id,
                MIN(conversation_messages.created_at)
            FROM tickets
            INNER JOIN conversation_messages
                ON conversation_messages.ticket_id = tickets.id
            GROUP BY tickets.id, tickets.user_id
        """)
    )

    # 4. Associa cada mensagem antiga à conversa do seu ticket.
    connection.execute(
        sa.text("""
            UPDATE conversation_messages
            SET conversation_id = (
                SELECT conversations.id
                FROM conversations
                WHERE conversations.ticket_id =
                    conversation_messages.ticket_id
            )
        """)
    )

    # 5. Confere se todas as mensagens foram associadas.
    pending_messages = connection.execute(
        sa.text("""
            SELECT COUNT(*)
            FROM conversation_messages
            WHERE conversation_id IS NULL
        """)
    ).scalar_one()

    if pending_messages > 0:
        raise RuntimeError(
            f"Existem {pending_messages} mensagens sem conversa. "
            "Migração interrompida para proteger os dados."
        )

    # 6. Ajusta a tabela existente usando batch, necessário no SQLite.
    with op.batch_alter_table(
        "conversation_messages",
        recreate="always",
    ) as batch_op:
        batch_op.alter_column(
            "conversation_id",
            existing_type=sa.Integer(),
            nullable=False,
        )

        batch_op.alter_column(
            "ticket_id",
            existing_type=sa.Integer(),
            nullable=True,
        )

        batch_op.create_foreign_key(
            "fk_conversation_messages_conversation_id_conversations",
            "conversations",
            ["conversation_id"],
            ["id"],
        )

        batch_op.create_index(
            "ix_conversation_messages_conversation_id",
            ["conversation_id"],
        )


def downgrade() -> None:
    connection = op.get_bind()

    # Não permite perder mensagens sem ticket ao voltar à estrutura antiga.
    messages_without_ticket = connection.execute(
        sa.text("""
            SELECT COUNT(*)
            FROM conversation_messages
            WHERE ticket_id IS NULL
        """)
    ).scalar_one()

    if messages_without_ticket > 0:
        raise RuntimeError(
            "Não é possível reverter: existem mensagens sem ticket. "
            "A estrutura antiga exigia ticket_id obrigatório."
        )

    # Remove a relação com conversations e restaura a estrutura anterior.
    with op.batch_alter_table(
        "conversation_messages",
        recreate="always",
    ) as batch_op:
        batch_op.drop_constraint(
            "fk_conversation_messages_conversation_id_conversations",
            type_="foreignkey",
        )

        batch_op.drop_index(
            "ix_conversation_messages_conversation_id"
        )

        batch_op.drop_column("conversation_id")

        batch_op.alter_column(
            "ticket_id",
            existing_type=sa.Integer(),
            nullable=False,
        )

    op.drop_index(
        "ix_conversations_user_id",
        table_name="conversations",
    )
    op.drop_index(
        "ix_conversations_ticket_id",
        table_name="conversations",
    )
    op.drop_table("conversations")
