"""DAOs: único lugar do sistema que executa SQL."""
import sqlite3
from models import Categoria, Tecnologia, Projeto, Mensagem


class BaseDAO:
    def __init__(self, db):
        self.db = db


class CategoriaDAO(BaseDAO):
    def listar(self):
        con = self.db.conectar()
        rows = con.execute("SELECT * FROM categoria ORDER BY id_categoria").fetchall()
        con.close()
        return [Categoria(**dict(r)) for r in rows]


class TecnologiaDAO(BaseDAO):
    def listar(self):
        con = self.db.conectar()
        rows = con.execute("SELECT * FROM tecnologia ORDER BY id_tecnologia").fetchall()
        con.close()
        return [Tecnologia(**dict(r)) for r in rows]


class ProjetoDAO(BaseDAO):
    _SQL = """SELECT p.*, c.nome AS categoria FROM projeto p
              JOIN categoria c ON c.id_categoria = p.id_categoria"""

    def _montar(self, con, row):
        techs = con.execute(
            """SELECT t.nome FROM tecnologia t
               JOIN projeto_tecnologia pt ON pt.id_tecnologia = t.id_tecnologia
               WHERE pt.id_projeto = ? ORDER BY t.id_tecnologia""", (row["id_projeto"],)).fetchall()
        return Projeto(**dict(row), tecnologias=[t["nome"] for t in techs])

    def listar(self):
        con = self.db.conectar()
        rows = con.execute(self._SQL + " ORDER BY p.id_projeto").fetchall()
        projetos = [self._montar(con, r) for r in rows]
        con.close()
        return projetos

    def buscar_por_id(self, id_projeto):
        con = self.db.conectar()
        row = con.execute(self._SQL + " WHERE p.id_projeto = ?", (id_projeto,)).fetchone()
        projeto = self._montar(con, row) if row else None
        con.close()
        return projeto


class MensagemDAO(BaseDAO):
    _SQL = """SELECT m.*, p.titulo AS projeto FROM mensagem m
              LEFT JOIN projeto p ON p.id_projeto = m.id_projeto"""

    def inserir(self, msg):
        """Cadastra e devolve o novo id. Lança ValueError se o projeto não existir."""
        con = self.db.conectar()
        try:
            cur = con.execute(
                "INSERT INTO mensagem (nome, email, mensagem, id_projeto) VALUES (?,?,?,?)",
                (msg.nome[:100], msg.email[:150], msg.mensagem, msg.id_projeto))
            con.commit()
            return cur.lastrowid
        except sqlite3.IntegrityError:
            raise ValueError("Projeto inexistente")
        finally:
            con.close()

    def listar(self):
        con = self.db.conectar()
        rows = con.execute(self._SQL + " ORDER BY m.data_envio DESC, m.id_mensagem DESC").fetchall()
        con.close()
        return [Mensagem(**dict(r)) for r in rows]

    def buscar_por_id(self, id_mensagem):
        con = self.db.conectar()
        row = con.execute(self._SQL + " WHERE m.id_mensagem = ?", (id_mensagem,)).fetchone()
        con.close()
        return Mensagem(**dict(row)) if row else None

    def atualizar(self, id_mensagem, msg):
        con = self.db.conectar()
        cur = con.execute("UPDATE mensagem SET nome=?, email=?, mensagem=? WHERE id_mensagem=?",
                          (msg.nome[:100], msg.email[:150], msg.mensagem, id_mensagem))
        con.commit()
        alterou = cur.rowcount > 0
        con.close()
        return alterou

    def excluir(self, id_mensagem):
        con = self.db.conectar()
        cur = con.execute("DELETE FROM mensagem WHERE id_mensagem=?", (id_mensagem,))
        con.commit()
        apagou = cur.rowcount > 0
        con.close()
        return apagou
