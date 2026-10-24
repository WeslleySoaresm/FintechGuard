from getpass import getpass
import bcrypt
from sqlmodel import Session
from models.model_events import User
from data.db import engine
import sys
import os

# Adiciona a raiz do projeto ao PYTHONPATH do Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def create_user():
    print("=== Criar usuário FintechGuard ===")

    name = input("Nome: ").strip()
    email = input("E-mail: ").strip().lower()

    password = getpass("Senha: ")
    password_confirmation = getpass("Confirme a senha: ")

    # ---------------------------------------------------------
    # Seleção de Role (Perfil)
    # ---------------------------------------------------------
    print("\nSelecione o Perfil (Role) do usuário:")
    roles_disponiveis = ["ADMIN", "GERENTE", "BANCARIO", "CUSTOMER"]
    
    for i, r in enumerate(roles_disponiveis, 1):
        print(f"[{i}] {r}")
        
    escolha = input("Escolha o número correspondente (Padrão [4] CUSTOMER): ").strip()
    
    role = "CUSTOMER" # Valor padrão caso o usuário apenas dê Enter
    if escolha.isdigit():
        idx = int(escolha) - 1
        if 0 <= idx < len(roles_disponiveis):
            role = roles_disponiveis[idx]
    elif escolha.upper() in roles_disponiveis:
        role = escolha.upper()

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
            role=role
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