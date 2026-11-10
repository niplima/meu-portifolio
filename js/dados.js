// Camada de dados do portfólio.
// 1) Com o servidor Flask (python app.py): usa a API /api/... e o banco SQLite.
// 2) Sem servidor (GitHub Pages / arquivo aberto direto): modo demonstração,
//    guardando as mensagens no localStorage do navegador.
const Dados = (function () {
    const BASE = location.pathname.includes('/pages/') ? '../' : '';
    const PROJETOS_PADRAO = [
  {
    "id_projeto": 1,
    "titulo": "Projeto 1: E-commerce Responsivo",
    "descricao": "Desenvolvimento de uma interface web para e-commerce utilizando HTML5, CSS3 e manipulação de DOM com JavaScript. O sistema possui navegação otimizada para dispositivos móveis e computadores.",
    "imagem": "img/projeto1.jpg",
    "link_repositorio": null,
    "destaque": 1,
    "categoria": "Web",
    "tecnologias": "HTML, CSS, JavaScript"
  },
  {
    "id_projeto": 2,
    "titulo": "Projeto 2: Aplicativo de Gestão de Tarefas",
    "descricao": "Sistema interativo de painel de controle (Dashboard) para gerenciamento de fluxo de trabalho diário. Conta com recursos de criação, edição e remoção de tarefas em tempo real.",
    "imagem": "img/projeto2.jpg",
    "link_repositorio": null,
    "destaque": 1,
    "categoria": "Aplicativo",
    "tecnologias": "HTML, CSS, JavaScript, LocalStorage"
  }
];
    let modoServidor = null;

    function detectar() {
        if (modoServidor === null) {
            modoServidor = fetch(BASE + 'api/projetos')
                .then(function (r) { return r.ok && (r.headers.get('content-type') || '').includes('json'); })
                .catch(function () { return false; });
        }
        return modoServidor;
    }

    function lerLocal() {
        try { return JSON.parse(localStorage.getItem('mensagens') || '[]'); } catch (e) { return []; }
    }
    function gravarLocal(lista) {
        try { localStorage.setItem('mensagens', JSON.stringify(lista)); } catch (e) {}
    }
    function enviarJson(url, metodo, corpo) {
        return fetch(BASE + url, {
            method: metodo,
            headers: { 'Content-Type': 'application/json' },
            body: corpo ? JSON.stringify(corpo) : undefined
        }).then(function (r) { if (!r.ok) throw new Error('Falha'); return r.json(); });
    }

    return {
        modoServidor: detectar,
        listarProjetos: function () {
            return detectar().then(function (srv) {
                if (!srv) return PROJETOS_PADRAO;
                return fetch(BASE + 'api/projetos').then(function (r) { return r.json(); });
            });
        },
        listarMensagens: function () {
            return detectar().then(function (srv) {
                if (srv) return fetch(BASE + 'api/mensagens').then(function (r) { return r.json(); });
                return lerLocal();
            });
        },
        enviarMensagem: function (d) {
            return detectar().then(function (srv) {
                if (srv) return enviarJson('api/mensagens', 'POST', d);
                const lista = lerLocal();
                const proj = PROJETOS_PADRAO.find(function (p) { return String(p.id_projeto) === String(d.id_projeto); });
                lista.unshift({
                    id_mensagem: Date.now(), nome: d.nome, email: d.email, mensagem: d.mensagem,
                    data_envio: new Date().toLocaleString('pt-BR'),
                    id_projeto: d.id_projeto || null, projeto: proj ? proj.titulo : null
                });
                gravarLocal(lista);
                return { ok: true };
            });
        },
        editarMensagem: function (id, d) {
            return detectar().then(function (srv) {
                if (srv) return enviarJson('api/mensagens/' + id, 'PUT', d);
                const lista = lerLocal();
                lista.forEach(function (m) {
                    if (String(m.id_mensagem) === String(id)) { m.nome = d.nome; m.email = d.email; m.mensagem = d.mensagem; }
                });
                gravarLocal(lista);
                return { ok: true };
            });
        },
        excluirMensagem: function (id) {
            return detectar().then(function (srv) {
                if (srv) return enviarJson('api/mensagens/' + id, 'DELETE');
                gravarLocal(lerLocal().filter(function (m) { return String(m.id_mensagem) !== String(id); }));
                return { ok: true };
            });
        }
    };
})();
