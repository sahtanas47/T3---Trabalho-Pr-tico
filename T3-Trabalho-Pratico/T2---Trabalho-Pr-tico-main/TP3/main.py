from sqlalchemy import select

import criar_banco
from consultas import mostrar_consultas
from database import engine, Session
from models import Base, Prateleira, Item, Livro, HQ, Usuario


def pedir_int(texto):
    while True:
        try:
            return int(input(texto))
        except ValueError:
            print("Digite apenas números.")


def buscar_ou_criar_prateleira(session, codigo):
    prateleira = session.scalar(select(Prateleira).where(Prateleira.codigo == codigo))
    if prateleira is None:
        prateleira = Prateleira(codigo=codigo)
        session.add(prateleira)
    return prateleira


def cadastrar_livro(session):
    titulo = input("Título do livro: ")
    ano = pedir_int("Ano: ")
    autor = input("Autor: ")
    paginas = pedir_int("Páginas: ")
    prateleira = buscar_ou_criar_prateleira(session, input("Prateleira (ex.: A1): "))
    session.add(Livro(titulo=titulo, ano=ano, autor=autor, num_paginas=paginas, prateleira=prateleira))
    session.commit()
    print("Livro adicionado com sucesso!")


def cadastrar_hq(session):
    titulo = input("Título da HQ: ")
    ano = pedir_int("Ano: ")
    edicao = pedir_int("Edição nº: ")
    autor = input("Autor: ")
    prateleira = buscar_ou_criar_prateleira(session, input("Prateleira (ex.: A1): "))
    session.add(HQ(titulo=titulo, ano=ano, autor=autor, edicao=edicao, prateleira=prateleira))
    session.commit()
    print("HQ adicionada com sucesso!")


def cadastrar_usuario(session):
    nome = input("Digite o nome: ")
    cpf = input("Digite o CPF (só números): ")
    if session.scalar(select(Usuario).where(Usuario.cpf == cpf)) is not None:
        print("Já existe um usuário com esse CPF!")
        return
    session.add(Usuario(nome=nome, cpf=cpf))
    session.commit()
    print("Usuário cadastrado com sucesso!")


def listar_itens(session):
    codigo = input("Código da prateleira (ex.: A1): ")
    prateleira = session.scalar(select(Prateleira).where(Prateleira.codigo == codigo))
    if prateleira is None:
        print("Prateleira não encontrada.")
        return
    print(f"\nItens na prateleira {prateleira.codigo}:")
    for item in prateleira.itens:
        status = "Emprestado" if item.usuarios else "Disponível"
        if item.tipo == 'livro':
            extra = f"LIVRO | Autor: {item.autor} | Páginas: {item.num_paginas}"
        else:
            extra = f"HQ | Autor: {item.autor} | Edição nº: {item.edicao}"
        print(f"  [{item.id}] {item.titulo} ({item.ano}) | {extra} | {status}")


def listar_usuarios(session):
    for usuario in session.scalars(select(Usuario)).all():
        print(f"[{usuario.id}] {usuario.nome} (CPF: {usuario.cpf})")


def realizar_emprestimo(session):
    usuarios = session.scalars(select(Usuario)).all()
    disponiveis = [item for item in session.scalars(select(Item)).all() if not item.usuarios]
    if not usuarios or not disponiveis:
        print("É preciso ter pelo menos 1 usuário e 1 item disponível!")
        return

    print("Usuários:")
    for usuario in usuarios:
        print(f"  [{usuario.id}] {usuario.nome}")
    id_usuario = pedir_int("Digite o id do usuário: ")
    usuario = session.scalar(select(Usuario).where(Usuario.id == id_usuario))

    print("Itens disponíveis:")
    for item in disponiveis:
        print(f"  [{item.id}] {item.titulo} (prateleira {item.prateleira.codigo})")
    id_item = pedir_int("Digite o id do item: ")
    item = session.scalar(select(Item).where(Item.id == id_item))

    if usuario is None or item is None:
        print("Usuário ou item não encontrado.")
    elif item.usuarios:
        print("Este item já está emprestado!")
    else:
        item.usuarios.append(usuario)  # grava o par na tabela 'emprestimos'
        session.commit()
        print("Empréstimo realizado com sucesso!")


def listar_emprestimos(session):
    pares = []
    for item in session.scalars(select(Item)).all():
        for usuario in item.usuarios:
            pares.append((usuario, item))
    if not pares:
        print("Não há nenhum empréstimo ativo.")
    for numero, (usuario, item) in enumerate(pares):
        print(f"  {numero} - {usuario.nome} está com '{item.titulo}'")
    return pares


def devolver_emprestimo(session):
    pares = listar_emprestimos(session)
    if not pares:
        return
    numero = pedir_int("Digite o número do empréstimo a ser devolvido: ")
    if numero < 0 or numero >= len(pares):
        print("Esse empréstimo não existe!")
        return
    usuario, item = pares[numero]
    item.usuarios.remove(usuario)  
    session.commit()
    print("Empréstimo finalizado!")


def main():
    Base.metadata.create_all(engine) 
    session = Session()
    if session.scalar(select(Prateleira)) is None: 
        session.close()
        criar_banco.popular()
        session = Session()

    while True:
        print("\n--- MENU DA BIBLIOTECA ---")
        print("1. Cadastrar Livro")
        print("2. Cadastrar HQ")
        print("3. Cadastrar Usuário")
        print("4. Realizar Empréstimo")
        print("5. Listar Itens da Prateleira")
        print("6. Listar Empréstimos")
        print("7. Devolver Empréstimo")
        print("8. Listar Usuários")
        print("9. Mostrar as 3 consultas")
        print("10. Recriar o banco com dados de exemplo")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_livro(session)
        elif opcao == "2":
            cadastrar_hq(session)
        elif opcao == "3":
            cadastrar_usuario(session)
        elif opcao == "4":
            realizar_emprestimo(session)
        elif opcao == "5":
            listar_itens(session)
        elif opcao == "6":
            listar_emprestimos(session)
        elif opcao == "7":
            devolver_emprestimo(session)
        elif opcao == "8":
            listar_usuarios(session)
        elif opcao == "9":
            mostrar_consultas(session)
        elif opcao == "10":
            session.close()
            criar_banco.criar_tabelas()
            criar_banco.popular()
            session = Session()
        elif opcao == "0":
            print("Saindo do programa...")
            break
        else:
            print("ERRO! Opção inválida. Tente novamente.")

    session.close()


if __name__ == "__main__":
    main()
