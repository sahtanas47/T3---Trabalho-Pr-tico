from database import engine, Session
from models import Base, Prateleira, Item, Livro, HQ, Usuario


def criar_tabelas():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print("Tabelas criadas: prateleiras, itens, usuarios, emprestimos")


def popular():
    session = Session()

    a1 = Prateleira(codigo='A1')
    b1 = Prateleira(codigo='B1')
    c1 = Prateleira(codigo='C1')

    sarah = Usuario(nome='Sarah Sodre', cpf='11111111111')
    beatriz = Usuario(nome='Beatriz Martins Cangue', cpf='22222222222')
    joao = Usuario(nome='João Silva', cpf='33333333333')
    maria = Usuario(nome='Maria Souza', cpf='44444444444')
    pedro = Usuario(nome='Pedro Lima', cpf='55555555555')

    itens = [
        Livro(titulo='Dom Casmurro', ano=1899, autor='Machado de Assis',
              num_paginas=256, prateleira=a1, usuarios=[sarah]),
        Livro(titulo='Memórias Póstumas de Brás Cubas', ano=1881, autor='Machado de Assis',
              num_paginas=368, prateleira=a1, usuarios=[beatriz]),
        HQ(titulo='Ultimate Wolverine', ano=2026, autor='Desconhecido',
           edicao=2, prateleira=a1, usuarios=[sarah]),
        Livro(titulo='Dom Quixote', ano=1605, autor='Miguel de Cervantes',
              num_paginas=863, prateleira=b1, usuarios=[maria]),
        HQ(titulo='Batman: A Piada Mortal', ano=1988, autor='Alan Moore',
           edicao=1, prateleira=b1, usuarios=[sarah]),
        HQ(titulo='Watchmen', ano=1986, autor='Alan Moore',
           edicao=1, prateleira=b1),
    ]

    session.add_all(itens)
    session.add_all([c1, joao, pedro])
    session.commit()
    session.close()
    print("Dados cadastrados!")


if __name__ == "__main__":
    criar_tabelas()
    popular()
