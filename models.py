"""Classes de modelo (entidades do banco)."""
import re


class Categoria:
    def __init__(self, id_categoria, nome, descricao=None):
        self.id_categoria = id_categoria
        self.nome = nome
        self.descricao = descricao

    def to_dict(self):
        return dict(self.__dict__)


class Tecnologia:
    def __init__(self, id_tecnologia, nome):
        self.id_tecnologia = id_tecnologia
        self.nome = nome

    def to_dict(self):
        return dict(self.__dict__)


class Projeto:
    def __init__(self, id_projeto, titulo, descricao, imagem, link_repositorio,
                 destaque, data_criacao, id_categoria, categoria=None, tecnologias=None):
        self.id_projeto = id_projeto
        self.titulo = titulo
        self.descricao = descricao
        self.imagem = imagem
        self.link_repositorio = link_repositorio
        self.destaque = destaque
        self.data_criacao = data_criacao
        self.id_categoria = id_categoria
        self.categoria = categoria
        self.tecnologias = tecnologias or []

    def to_dict(self):
        d = dict(self.__dict__)
        d["tecnologias"] = ", ".join(self.tecnologias)  # formato usado pelo front-end
        return d


class Mensagem:
    def __init__(self, id_mensagem=None, nome="", email="", mensagem="",
                 data_envio=None, id_projeto=None, projeto=None):
        self.id_mensagem = id_mensagem
        self.nome = (nome or "").strip()
        self.email = (email or "").strip()
        self.mensagem = (mensagem or "").strip()
        self.data_envio = data_envio
        self.id_projeto = id_projeto or None
        self.projeto = projeto

    def validar(self):
        """True se nome, e-mail e mensagem estão preenchidos corretamente."""
        email_ok = re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", self.email) is not None
        return bool(self.nome) and bool(self.mensagem) and email_ok

    def to_dict(self):
        return dict(self.__dict__)
