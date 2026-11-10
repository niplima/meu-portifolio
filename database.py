"""Conexão e criação do banco (SQLite). Mesma estrutura do modelo físico (banco/portfolio.sql)."""
import os
import sqlite3

BASE = os.path.dirname(os.path.abspath(__file__))

SCHEMA = """
CREATE TABLE IF NOT EXISTS categoria (
    id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
    nome         VARCHAR(60) NOT NULL UNIQUE,
    descricao    VARCHAR(255)
);
CREATE TABLE IF NOT EXISTS projeto (
    id_projeto       INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo           VARCHAR(100) NOT NULL UNIQUE,
    descricao        TEXT NOT NULL,
    imagem           VARCHAR(255),
    link_repositorio VARCHAR(255),
    destaque         TINYINT NOT NULL DEFAULT 0 CHECK (destaque IN (0,1)),
    data_criacao     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    id_categoria     INTEGER NOT NULL REFERENCES categoria(id_categoria)
                     ON UPDATE CASCADE ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS tecnologia (
    id_tecnologia INTEGER PRIMARY KEY AUTOINCREMENT,
    nome          VARCHAR(50) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS projeto_tecnologia (
    id_projeto    INTEGER NOT NULL REFERENCES projeto(id_projeto) ON UPDATE CASCADE ON DELETE CASCADE,
    id_tecnologia INTEGER NOT NULL REFERENCES tecnologia(id_tecnologia) ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (id_projeto, id_tecnologia)
);
CREATE TABLE IF NOT EXISTS mensagem (
    id_mensagem INTEGER PRIMARY KEY AUTOINCREMENT,
    nome        VARCHAR(100) NOT NULL,
    email       VARCHAR(150) NOT NULL,
    mensagem    TEXT NOT NULL,
    data_envio  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    id_projeto  INTEGER REFERENCES projeto(id_projeto) ON UPDATE CASCADE ON DELETE SET NULL
);
"""

SEED = """
INSERT INTO categoria (nome, descricao) VALUES
  ('Web', 'Sites e sistemas executados no navegador'),
  ('Aplicativo', 'Sistemas interativos de gestão e produtividade');
INSERT INTO tecnologia (nome) VALUES ('HTML'),('CSS'),('JavaScript'),('LocalStorage'),('PHP'),('MySQL');
INSERT INTO projeto (titulo, descricao, imagem, destaque, id_categoria) VALUES
  ('Projeto 1: E-commerce Responsivo',
   'Desenvolvimento de uma interface web para e-commerce utilizando HTML5, CSS3 e manipulação de DOM com JavaScript. O sistema possui navegação otimizada para dispositivos móveis e computadores.',
   'img/projeto1.jpg', 1, 1),
  ('Projeto 2: Aplicativo de Gestão de Tarefas',
   'Sistema interativo de painel de controle (Dashboard) para gerenciamento de fluxo de trabalho diário. Conta com recursos de criação, edição e remoção de tarefas em tempo real.',
   'img/projeto2.jpg', 1, 2);
INSERT INTO projeto_tecnologia VALUES (1,1),(1,2),(1,3),(2,1),(2,2),(2,3),(2,4);
"""


class Database:
    """Responsável por abrir conexões e criar/popular o banco."""

    def __init__(self, caminho=None):
        self.caminho = caminho or os.path.join(BASE, "portfolio.db")

    def conectar(self):
        con = sqlite3.connect(self.caminho)
        con.row_factory = sqlite3.Row
        con.execute("PRAGMA foreign_keys = ON")
        return con

    def iniciar(self):
        novo = not os.path.exists(self.caminho)
        con = self.conectar()
        con.executescript(SCHEMA)
        if novo:
            con.executescript(SEED)
        con.commit()
        con.close()
