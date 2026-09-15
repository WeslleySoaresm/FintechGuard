from getpass import getpass
import bcrypt
from sqlmodel import Session
from models.model_events import User
from data.db import engine


# Configuração para geração e verificação de senhas com bcrypt



def create_user():
    print("=== Criar usuário FintechGuard ===")

    name = input("Nome: ").strip()
    email = input("E-mail: ").strip().lower()

    password = getpass("Senha: ")
    password_confirmation = getpass("Confirme a senha: ")

    # ---------------------------------------------------------
    # Validações básicas
    # ---------------------------------------------------------

    if not name:
        print("Erro: o nome não pode estar vazio.")
        return

    if not email:
        print("Erro: o e-mail não pode estar vazio.")
        return

    if not password:
        print("Erro: a senha não pode estar vazia.")
        return

    if password != password_confirmation:
        print("Erro: as senhas não coincidem.")
        return

    # ---------------------------------------------------------
    # Cria o hash da senha
    # ---------------------------------------------------------

    password_hash = bcrypt.hashpw(
    password.encode("utf-8"),
    bcrypt.gensalt()
    ).decode("utf-8")

    # ---------------------------------------------------------
    # Salva o usuário no banco
    # ---------------------------------------------------------

    with Session(engine) as session:

        user = User(
            name=name,
            email=email,
            password_hash=password_hash,
            role="CUSTOMER"
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        print()
        print("Usuário criado com sucesso!")
        print(f"ID: {user.id}")
        print(f"Nome: {user.name}")
        print(f"E-mail: {user.email}")
        print(f"Role: {user.role}")


if __name__ == "__main__":
    create_user()