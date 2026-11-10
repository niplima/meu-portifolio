-- =====================================================================
-- MODELO FÍSICO - Banco de dados do Portfólio de Nicolas
-- SGBD: MySQL 8 / MariaDB (compatível com XAMPP)
-- Como executar: phpMyAdmin > Importar, ou  mysql -u root < modelo_fisico.sql
-- =====================================================================

DROP DATABASE IF EXISTS portfolio;
CREATE DATABASE portfolio
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
USE portfolio;

-- ---------------------------------------------------------------------
-- Tabela: categoria  (1 categoria  -> N projetos)
-- ---------------------------------------------------------------------
CREATE TABLE categoria (
    id_categoria  INT          NOT NULL AUTO_INCREMENT,
    nome          VARCHAR(60)  NOT NULL,
    descricao     VARCHAR(255) NULL,
    CONSTRAINT pk_categoria PRIMARY KEY (id_categoria),
    CONSTRAINT uq_categoria_nome UNIQUE (nome)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Tabela: projeto  (N projetos <-> N tecnologias via projeto_tecnologia)
-- ---------------------------------------------------------------------
CREATE TABLE projeto (
    id_projeto       INT          NOT NULL AUTO_INCREMENT,
    titulo           VARCHAR(100) NOT NULL,
    descricao        TEXT         NOT NULL,
    imagem           VARCHAR(255) NULL,
    link_repositorio VARCHAR(255) NULL,
    destaque         TINYINT(1)   NOT NULL DEFAULT 0,
    data_criacao     DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    id_categoria     INT          NOT NULL,
    CONSTRAINT pk_projeto PRIMARY KEY (id_projeto),
    CONSTRAINT uq_projeto_titulo UNIQUE (titulo),
    CONSTRAINT ck_projeto_destaque CHECK (destaque IN (0, 1)),
    CONSTRAINT fk_projeto_categoria FOREIGN KEY (id_categoria)
        REFERENCES categoria (id_categoria)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Tabela: tecnologia
-- ---------------------------------------------------------------------
CREATE TABLE tecnologia (
    id_tecnologia INT         NOT NULL AUTO_INCREMENT,
    nome          VARCHAR(50) NOT NULL,
    CONSTRAINT pk_tecnologia PRIMARY KEY (id_tecnologia),
    CONSTRAINT uq_tecnologia_nome UNIQUE (nome)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Tabela associativa: projeto_tecnologia  (resolve o relacionamento N:N)
-- ---------------------------------------------------------------------
CREATE TABLE projeto_tecnologia (
    id_projeto    INT NOT NULL,
    id_tecnologia INT NOT NULL,
    CONSTRAINT pk_projeto_tecnologia PRIMARY KEY (id_projeto, id_tecnologia),
    CONSTRAINT fk_pt_projeto FOREIGN KEY (id_projeto)
        REFERENCES projeto (id_projeto)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_pt_tecnologia FOREIGN KEY (id_tecnologia)
        REFERENCES tecnologia (id_tecnologia)
        ON UPDATE CASCADE
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Tabela: mensagem  (formulário de contato; projeto de interesse é opcional)
-- ---------------------------------------------------------------------
CREATE TABLE mensagem (
    id_mensagem INT          NOT NULL AUTO_INCREMENT,
    nome        VARCHAR(100) NOT NULL,
    email       VARCHAR(150) NOT NULL,
    mensagem    TEXT         NOT NULL,
    data_envio  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    id_projeto  INT          NULL,
    CONSTRAINT pk_mensagem PRIMARY KEY (id_mensagem),
    CONSTRAINT fk_mensagem_projeto FOREIGN KEY (id_projeto)
        REFERENCES projeto (id_projeto)
        ON UPDATE CASCADE
        ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE INDEX idx_projeto_categoria ON projeto (id_categoria);
CREATE INDEX idx_mensagem_projeto  ON mensagem (id_projeto);

-- ---------------------------------------------------------------------
-- Dados iniciais (os mesmos projetos exibidos no site)
-- ---------------------------------------------------------------------
INSERT INTO categoria (nome, descricao) VALUES
    ('Web',      'Sites e sistemas executados no navegador'),
    ('Aplicativo', 'Sistemas interativos de gestão e produtividade');

INSERT INTO tecnologia (nome) VALUES
    ('HTML'), ('CSS'), ('JavaScript'), ('LocalStorage'), ('PHP'), ('MySQL');

INSERT INTO projeto (titulo, descricao, imagem, destaque, id_categoria) VALUES
    ('Projeto 1: E-commerce Responsivo',
     'Desenvolvimento de uma interface web para e-commerce utilizando HTML5, CSS3 e manipulação de DOM com JavaScript. O sistema possui navegação otimizada para dispositivos móveis e computadores.',
     'img/projeto1.jpg', 1, 1),
    ('Projeto 2: Aplicativo de Gestão de Tarefas',
     'Sistema interativo de painel de controle (Dashboard) para gerenciamento de fluxo de trabalho diário. Conta com recursos de criação, edição e remoção de tarefas em tempo real.',
     'img/projeto2.jpg', 1, 2);

INSERT INTO projeto_tecnologia (id_projeto, id_tecnologia) VALUES
    (1, 1), (1, 2), (1, 3),
    (2, 1), (2, 2), (2, 3), (2, 4);
