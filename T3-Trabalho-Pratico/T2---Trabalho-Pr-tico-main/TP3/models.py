from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

emprestimos = Table(
    'emprestimos', Base.metadata,
    Column('usuario_id', Integer, ForeignKey('usuarios.id'), primary_key=True),
    Column('item_id', Integer, ForeignKey('itens.id'), primary_key=True),
)


class Prateleira(Base):
    __tablename__ = 'prateleiras'
    id = Column(Integer, primary_key=True)
    codigo = Column(String)

    itens = relationship('Item', back_populates='prateleira')

    def __repr__(self):
        return f"Prateleira({self.id}, {self.codigo!r})"


class Item(Base):
    __tablename__ = 'itens'
    id = Column(Integer, primary_key=True)
    titulo = Column(String)
    ano = Column(Integer)
    autor = Column(String)
    tipo = Column(String) 

    prateleira_id = Column(Integer, ForeignKey('prateleiras.id'))
    prateleira = relationship('Prateleira', back_populates='itens')   

    usuarios = relationship('Usuario', secondary=emprestimos, back_populates='itens')

    __mapper_args__ = {'polymorphic_on': tipo, 'polymorphic_identity': 'item'}

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id}, {self.titulo!r})"


class Livro(Item):
    num_paginas = Column(Integer)  # coluna só dos livros
    __mapper_args__ = {'polymorphic_identity': 'livro'}


class HQ(Item):
    edicao = Column(Integer)  
    __mapper_args__ = {'polymorphic_identity': 'hq'}


class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(String)

    itens = relationship('Item', secondary=emprestimos, back_populates='usuarios')

    def __repr__(self):
        return f"Usuario({self.id}, {self.nome!r})"
