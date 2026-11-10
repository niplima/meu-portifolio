"""Servidor do portfólio (Flask + SQLite).
Rodar:  pip install flask   e depois   python app.py   ->  http://localhost:5000
O banco (portfolio.db) é criado sozinho na primeira execução, com a mesma
estrutura do modelo físico (banco/portfolio.sql, versão MySQL)."""
import os
import re
import sqlite3
from flask import Flask, jsonify, request, send_from_directory, abort

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "portfolio.db")
app = Flask(__name__)

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


def conectar():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con


def iniciar_banco():
    novo = not os.path.exists(DB)
    con = conectar()
    con.executescript(SCHEMA)
    if novo:
        con.executescript(SEED)
    con.commit()
    con.close()


# ---------------- API ----------------
@app.get("/api/projetos")
def projetos():
    con = conectar()
    rows = con.execute("""
        SELECT p.id_projeto, p.titulo, p.descricao, p.imagem, p.link_repositorio, p.destaque,
               c.nome AS categoria,
               GROUP_CONCAT(t.nome, ', ') AS tecnologias
        FROM projeto p
        JOIN categoria c ON c.id_categoria = p.id_categoria
        LEFT JOIN projeto_tecnologia pt ON pt.id_projeto = p.id_projeto
        LEFT JOIN tecnologia t ON t.id_tecnologia = pt.id_tecnologia
        GROUP BY p.id_projeto ORDER BY p.id_projeto""").fetchall()
    con.close()
    return jsonify([dict(r) for r in rows])


def dados_validos(d):
    nome = (d.get("nome") or "").strip()
    email = (d.get("email") or "").strip()
    msg = (d.get("mensagem") or "").strip()
    if not nome or not msg or not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        return None
    return nome[:100], email[:150], msg


@app.get("/api/mensagens")
def listar_mensagens():
    con = conectar()
    rows = con.execute("""
        SELECT m.id_mensagem, m.nome, m.email, m.mensagem, m.data_envio, m.id_projeto,
               p.titulo AS projeto
        FROM mensagem m LEFT JOIN projeto p ON p.id_projeto = m.id_projeto
        ORDER BY m.data_envio DESC, m.id_mensagem DESC""").fetchall()
    con.close()
    return jsonify([dict(r) for r in rows])


@app.post("/api/mensagens")
def criar_mensagem():
    d = request.get_json(silent=True) or {}
    v = dados_validos(d)
    if not v:
        return jsonify(erro="Dados inválidos"), 400
    id_projeto = d.get("id_projeto") or None
    con = conectar()
    try:
        cur = con.execute("INSERT INTO mensagem (nome,email,mensagem,id_projeto) VALUES (?,?,?,?)",
                          (*v, id_projeto))
        con.commit()
    except sqlite3.IntegrityError:
        con.close()
        return jsonify(erro="Projeto inexistente"), 400
    con.close()
    return jsonify(id_mensagem=cur.lastrowid), 201


@app.put("/api/mensagens/<int:id_>")
def editar_mensagem(id_):
    v = dados_validos(request.get_json(silent=True) or {})
    if not v:
        return jsonify(erro="Dados inválidos"), 400
    con = conectar()
    con.execute("UPDATE mensagem SET nome=?, email=?, mensagem=? WHERE id_mensagem=?", (*v, id_))
    con.commit()
    con.close()
    return jsonify(ok=True)


@app.delete("/api/mensagens/<int:id_>")
def excluir_mensagem(id_):
    con = conectar()
    con.execute("DELETE FROM mensagem WHERE id_mensagem=?", (id_,))
    con.commit()
    con.close()
    return jsonify(ok=True)


# ---------------- Arquivos do site ----------------
PERMITIDOS = ("css", "js", "img", "pages")


@app.get("/")
def home():
    return send_from_directory(BASE, "index.html")


@app.get("/<path:caminho>")
def arquivos(caminho):
    if caminho.split("/")[0] not in PERMITIDOS:
        abort(404)
    return send_from_directory(BASE, caminho)


if __name__ == "__main__":
    iniciar_banco()
    app.run(debug=True)
