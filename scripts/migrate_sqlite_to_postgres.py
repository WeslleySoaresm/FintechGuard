
import argparse
import os
import sqlite3
import sys
from datetime import date, datetime
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import (
    Date,
    DateTime,
    MetaData,
    Table,
    create_engine,
    insert,
    select,
    text,
)


BASE_DIR = Path(__file__).resolve().parents[1]
SQLITE_PATH = BASE_DIR / "fintechguard.db"

TABLE_NAMES = [
    "users",
    "tickets",
    "conversations",
    "conversation_messages",
]


class MigrationError(Exception):
    pass


def get_database_url():
    load_dotenv(BASE_DIR / ".env")

    url = os.getenv("DATABASE_URL")

    if not url:
        raise MigrationError(
            "DATABASE_URL não encontrada. Configure a variável "
            "no terminal antes de executar."
        )

    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)

    return url


def read_sqlite_data():
    if not SQLITE_PATH.exists():
        raise MigrationError(
            f"Banco SQLite não encontrado: {SQLITE_PATH}"
        )

    source = sqlite3.connect(
        f"file:{SQLITE_PATH}?mode=ro",
        uri=True,
    )

    source.row_factory = sqlite3.Row

    try:
        data = {}

        for name in TABLE_NAMES:
            rows = source.execute(
                f'SELECT * FROM "{name}"'
            ).fetchall()

            data[name] = [
                dict(row)
                for row in rows
            ]

        return data

    finally:
        source.close()


def convert_value(value, column):
    if value is None:
        return None

    if isinstance(column.type, DateTime) and isinstance(value, str):
        return datetime.fromisoformat(
            value.replace("Z", "+00:00")
        )

    if isinstance(column.type, Date) and isinstance(value, str):
        return date.fromisoformat(value[:10])

    return value


def prepare_record(source_record, destination_table):
    record = {}

    for column in destination_table.columns:
        if column.name in source_record:
            record[column.name] = convert_value(
                source_record[column.name],
                column,
            )

    return record


def validate_source(data):
    users = data["users"]
    tickets = data["tickets"]
    conversations = data["conversations"]
    messages = data["conversation_messages"]

    user_ids = {row["id"] for row in users}
    ticket_ids = {row["id"] for row in tickets}
    conversation_ids = {row["id"] for row in conversations}

    emails = set()

    for user in users:
        email = user["email"].strip().lower()

        if email in emails:
            raise MigrationError(
                f"E-mail duplicado no SQLite: {user['email']}"
            )

        emails.add(email)

    for ticket in tickets:
        if ticket["user_id"] not in user_ids:
            raise MigrationError(
                f"Ticket {ticket['id']} possui usuário inexistente."
            )

    for conversation in conversations:
        if conversation["user_id"] not in user_ids:
            raise MigrationError(
                f"Conversa {conversation['id']} possui usuário inexistente."
            )

        ticket_id = conversation.get("ticket_id")

        if ticket_id is not None and ticket_id not in ticket_ids:
            raise MigrationError(
                f"Conversa {conversation['id']} possui ticket inexistente."
            )

    for message in messages:
        if message["conversation_id"] not in conversation_ids:
            raise MigrationError(
                f"Mensagem {message['id']} possui conversa inexistente."
            )

        ticket_id = message.get("ticket_id")

        if ticket_id is not None and ticket_id not in ticket_ids:
            raise MigrationError(
                f"Mensagem {message['id']} possui ticket inexistente."
            )


def validate_schema(source_data, destination_tables):
    for name, rows in source_data.items():
        source_columns = set(rows[0].keys()) if rows else set()

        destination_table = destination_tables[name]

        destination_columns = {
            column.name
            for column in destination_table.columns
        }

        missing = source_columns - destination_columns

        if missing:
            raise MigrationError(
                f"Colunas do SQLite ausentes em {name}: {missing}"
            )

        for column in destination_table.columns:
            if (
                column.name not in source_columns
                and not column.nullable
                and column.server_default is None
                and column.default is None
                and not column.primary_key
                and not column.autoincrement
            ):
                raise MigrationError(
                    f"Coluna obrigatória ausente: "
                    f"{name}.{column.name}"
                )


def migrate(execute=False):
    print("\n=== FINTECHGUARD: MIGRAÇÃO SQLITE → POSTGRESQL ===")

    print("\n1. Lendo banco SQLite...")

    data = read_sqlite_data()

    for name in TABLE_NAMES:
        print(f"   {name}: {len(data[name]):,} registros")

    validate_source(data)

    print("\n2. Conectando ao PostgreSQL...")

    engine = create_engine(
        get_database_url(),
        pool_pre_ping=True,
    )

    try:
        with engine.connect() as connection:
            transaction = connection.begin()

            try:
                metadata = MetaData()

                tables = {
                    name: Table(
                        name,
                        metadata,
                        autoload_with=connection,
                    )
                    for name in TABLE_NAMES
                }

                validate_schema(data, tables)

                # ---------------------------------------------
                # USUÁRIOS
                # ---------------------------------------------

                print("\n3. Verificando usuários...")

                users_table = tables["users"]

                remote_users = connection.execute(
                    select(
                        users_table.c.id,
                        users_table.c.email,
                    )
                ).mappings().all()

                remote_by_email = {
                    row["email"].strip().lower(): row["id"]
                    for row in remote_users
                }

                remote_user_ids = {
                    row["id"] for row in remote_users
                }

                user_id_map = {}
                users_to_insert = []

                for user in data["users"]:
                    email = user["email"].strip().lower()

                    if email in remote_by_email:
                        user_id_map[user["id"]] = remote_by_email[email]

                        print(
                            f"   Preservado: {email} "
                            f"(ID {remote_by_email[email]})"
                        )

                        continue

                    if user["id"] in remote_user_ids:
                        raise MigrationError(
                            f"ID de usuário {user['id']} já existe "
                            "com outro e-mail no PostgreSQL."
                        )

                    users_to_insert.append(
                        prepare_record(user, users_table)
                    )

                    user_id_map[user["id"]] = user["id"]

                if users_to_insert:
                    connection.execute(
                        insert(users_table),
                        users_to_insert,
                    )

                print(
                    f"   Novos usuários: {len(users_to_insert)}"
                )

                # ---------------------------------------------
                # TICKETS
                # ---------------------------------------------

                print("\n4. Importando tickets...")

                tickets_table = tables["tickets"]

                remote_ticket_ids = set(
                    connection.execute(
                        select(tickets_table.c.id)
                    ).scalars().all()
                )

                tickets_to_insert = []

                for ticket in data["tickets"]:
                    if ticket["id"] in remote_ticket_ids:
                        raise MigrationError(
                            f"Ticket ID {ticket['id']} já existe "
                            "no PostgreSQL."
                        )

                    record = prepare_record(
                        ticket,
                        tickets_table,
                    )

                    record["user_id"] = user_id_map[
                        ticket["user_id"]
                    ]

                    tickets_to_insert.append(record)

                if tickets_to_insert:
                    connection.execute(
                        insert(tickets_table),
                        tickets_to_insert,
                    )

                print(
                    f"   Tickets importados: {len(tickets_to_insert):,}"
                )

                # ---------------------------------------------
                # CONVERSAS
                # ---------------------------------------------

                print("\n5. Importando conversas...")

                conversations_table = tables["conversations"]

                conversation_id_map = {}

                for conversation in data["conversations"]:
                    record = prepare_record(
                        conversation,
                        conversations_table,
                    )

                    old_id = conversation["id"]

                    record.pop("id", None)

                    record["user_id"] = user_id_map[
                        conversation["user_id"]
                    ]

                    result = connection.execute(
                        insert(conversations_table)
                        .values(**record)
                        .returning(conversations_table.c.id)
                    )

                    conversation_id_map[old_id] = result.scalar_one()

                print(
                    f"   Conversas importadas: "
                    f"{len(conversation_id_map)}"
                )

                # ---------------------------------------------
                # MENSAGENS
                # ---------------------------------------------

                print("\n6. Importando mensagens...")

                messages_table = tables["conversation_messages"]

                for message in data["conversation_messages"]:
                    record = prepare_record(
                        message,
                        messages_table,
                    )

                    record.pop("id", None)

                    record["conversation_id"] = conversation_id_map[
                        message["conversation_id"]
                    ]

                    connection.execute(
                        insert(messages_table).values(**record)
                    )

                print(
                    f"   Mensagens importadas: "
                    f"{len(data['conversation_messages'])}"
                )

                # ---------------------------------------------
                # SEQUÊNCIAS
                # ---------------------------------------------

                if execute:
                    print("\n7. Atualizando sequências...")

                    for name in TABLE_NAMES:
                        sequence = connection.execute(
                            text(
                                "SELECT pg_get_serial_sequence("
                                ":table_name, 'id')"
                            ),
                            {"table_name": name},
                        ).scalar()

                        if not sequence:
                            continue

                        max_id = connection.execute(
                            text(f'SELECT MAX(id) FROM "{name}"')
                        ).scalar()

                        if max_id is None:
                            connection.execute(
                                text(
                                    "SELECT setval("
                                    "CAST(:sequence AS regclass), 1, false)"
                                ),
                                {"sequence": sequence},
                            )
                        else:
                            connection.execute(
                                text(
                                    "SELECT setval("
                                    "CAST(:sequence AS regclass), "
                                    ":max_id, true)"
                                ),
                                {
                                    "sequence": sequence,
                                    "max_id": max_id,
                                },
                            )

                # ---------------------------------------------
                # CONFERÊNCIA
                # ---------------------------------------------

                print("\n8. Conferindo totais...")

                for name in TABLE_NAMES:
                    total = connection.execute(
                        text(f'SELECT COUNT(*) FROM "{name}"')
                    ).scalar_one()

                    print(f"   {name}: {total:,}")

                if execute:
                    transaction.commit()
                    print("\nMIGRAÇÃO GRAVADA COM SUCESSO.")

                else:
                    transaction.rollback()
                    print(
                        "\nSIMULAÇÃO CONCLUÍDA. "
                        "Nenhuma alteração foi gravada."
                    )

            except Exception:
                if transaction.is_active:
                    transaction.rollback()

                raise

    finally:
        engine.dispose()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--execute",
        action="store_true",
        help="Confirma e grava a migração no PostgreSQL.",
    )

    args = parser.parse_args()

    try:
        migrate(execute=args.execute)

    except Exception as error:
        print(f"\nERRO: {error}", file=sys.stderr)
        sys.exit(1)
