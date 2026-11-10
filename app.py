"""Rotas Flask do portfólio (as rotas só chamam os DAOs).
Rodar:  pip install flask   e depois   python app.py   ->  http://localhost:5000"""
import os
from flask import Flask, jsonify, request, send_from_directory, abort

from database import Database
from daos import CategoriaDAO, TecnologiaDAO, ProjetoDAO, MensagemDAO
from models import Mensagem

BASE = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

db = Database()
categoria_dao = CategoriaDAO(db)
tecnologia_dao = TecnologiaDAO(db)
projeto_dao = ProjetoDAO(db)
mensagem_dao = MensagemDAO(db)


def lista_json(objetos):
    return jsonify([o.to_dict() for o in objetos])


# ---------------- API ----------------
@app.get("/api/categorias")
def api_categorias():
    return lista_json(categoria_dao.listar())


@app.get("/api/tecnologias")
def api_tecnologias():
    return lista_json(tecnologia_dao.listar())


@app.get("/api/projetos")
def api_projetos():
    return lista_json(projeto_dao.listar())


@app.get("/api/projetos/<int:id_>")
def api_projeto(id_):
    p = projeto_dao.buscar_por_id(id_)
    return (jsonify(p.to_dict()), 200) if p else (jsonify(erro="Projeto não encontrado"), 404)


@app.get("/api/mensagens")
def api_listar_mensagens():
    return lista_json(mensagem_dao.listar())


@app.get("/api/mensagens/<int:id_>")
def api_mensagem(id_):
    m = mensagem_dao.buscar_por_id(id_)
    return (jsonify(m.to_dict()), 200) if m else (jsonify(erro="Mensagem não encontrada"), 404)


@app.post("/api/mensagens")
def api_criar_mensagem():
    d = request.get_json(silent=True) or {}
    msg = Mensagem(nome=d.get("nome"), email=d.get("email"),
                   mensagem=d.get("mensagem"), id_projeto=d.get("id_projeto"))
    if not msg.validar():
        return jsonify(erro="Dados inválidos"), 400
    try:
        novo_id = mensagem_dao.inserir(msg)
    except ValueError as e:
        return jsonify(erro=str(e)), 400
    return jsonify(id_mensagem=novo_id), 201


@app.put("/api/mensagens/<int:id_>")
def api_editar_mensagem(id_):
    d = request.get_json(silent=True) or {}
    msg = Mensagem(nome=d.get("nome"), email=d.get("email"), mensagem=d.get("mensagem"))
    if not msg.validar():
        return jsonify(erro="Dados inválidos"), 400
    if not mensagem_dao.atualizar(id_, msg):
        return jsonify(erro="Mensagem não encontrada"), 404
    return jsonify(ok=True)


@app.delete("/api/mensagens/<int:id_>")
def api_excluir_mensagem(id_):
    if not mensagem_dao.excluir(id_):
        return jsonify(erro="Mensagem não encontrada"), 404
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
    db.iniciar()
    app.run(debug=True)
