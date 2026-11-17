from sqlalchemy import select, func, desc

from database import Session
from models import Prateleira, Item, Usuario


def consulta_1_emprestimos(session):
    query = select(Usuario.nome, Item.titulo).join(Usuario.itens).order_by(Usuario.nome)
    return session.execute(query).all()


def consulta_2_itens_por_prateleira(session):
    query = (
        select(Prateleira.codigo, func.count(Item.id).label("qtd"))
        .join(Prateleira.itens, isouter=True)
        .group_by(Prateleira.codigo)
    )
    return session.execute(query).all()


def consulta_3_usuarios_com_mais_itens(session):
    query = (
        select(Usuario.nome, func.count(Item.id).label("qtd"))
        .join(Usuario.itens)
        .group_by(Usuario.nome)
        .order_by(desc("qtd"))
    )
    return session.execute(query).all()


def mostrar_consultas(session):
    print("\n=== Consulta 1: empréstimos (usuário - item) ===")
    for linha in consulta_1_emprestimos(session):
        print(f"{linha.nome} está com '{linha.titulo}'")

    print("\n=== Consulta 2: quantidade de itens por prateleira ===")
    for linha in consulta_2_itens_por_prateleira(session):
        print(f"Prateleira {linha.codigo}: {linha.qtd} item(ns)")

    print("\n=== Consulta 3: usuários com mais itens emprestados ===")
    for linha in consulta_3_usuarios_com_mais_itens(session):
        print(f"{linha.nome}: {linha.qtd} item(ns)")


if __name__ == "__main__":
    session = Session()
    mostrar_consultas(session)
    session.close()
