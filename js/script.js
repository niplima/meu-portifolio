document.addEventListener('DOMContentLoaded', function () {
    
    // === 1. GALERIA DE IMAGENS INTERATIVA (Página Inicial e Projetos) ===
    const destaque = document.querySelector('#imagem-destaque');
    const legenda = document.querySelector('#legenda-destaque');
    const miniaturas = document.querySelectorAll('.miniatura');

    if (destaque && miniaturas.length > 0) {
        miniaturas.forEach(function (img) {
            img.addEventListener('click', function () {
                // Troca a imagem em destaque
                destaque.src = img.src;

                // Atualiza a legenda com o atributo 'alt' usando textContent
                if (legenda) {
                    legenda.textContent = img.getAttribute('alt') || 'Projeto em Destaque';
                }

                // Altera as classes dinamicamente usando classList
                miniaturas.forEach(function (m) {
                    m.classList.remove('ativa');
                });
                img.classList.add('ativa');
            });
        });
    }

    // === 2. FORMULÁRIO DE CONTATO (salva via Dados: Flask/SQLite ou modo demonstração) ===
    const formContato = document.querySelector('#form-contato');
    const mensagemFeedback = document.querySelector('#feedback-mensagem');

    function mostrar(texto, ok) {
        if (!mensagemFeedback) return;
        mensagemFeedback.textContent = texto;
        mensagemFeedback.classList.toggle('sucesso', ok);
        mensagemFeedback.classList.toggle('erro', !ok);
        mensagemFeedback.style.display = 'block';
    }

    if (formContato) {
        formContato.addEventListener('submit', function (event) {
            event.preventDefault();
            const dados = {
                nome: document.querySelector('#nome').value.trim(),
                email: document.querySelector('#email').value.trim(),
                mensagem: document.querySelector('#mensagem').value.trim(),
                id_projeto: document.querySelector('#id_projeto').value || null
            };
            Dados.enviarMensagem(dados)
                .then(function () {
                    mostrar('Obrigado, ' + dados.nome + '! Sua mensagem foi enviada com sucesso.', true);
                    formContato.reset();
                })
                .catch(function () { mostrar('Não foi possível enviar. Tente novamente.', false); });
        });
    }

    // === 3. PROJETOS VINDOS DO BANCO ===
    const grid = document.querySelector('#projetos-db');
    const select = document.querySelector('#id_projeto');
    const detalhado = location.pathname.includes('/pages/');
    const base = detalhado ? '../' : '';

    if (grid || select) {
        Dados.listarProjetos().then(function (projetos) {
            if (grid) {
                grid.innerHTML = '';
                projetos.forEach(function (p) {
                    const card = document.createElement('div');
                    card.className = 'project-card';
                    const h3 = document.createElement('h3');
                    h3.textContent = p.titulo;
                    card.appendChild(h3);
                    if (detalhado && p.imagem) {
                        const img = document.createElement('img');
                        img.src = base + p.imagem;
                        img.alt = p.titulo;
                        img.className = 'project-img';
                        card.appendChild(img);
                    }
                    const desc = document.createElement('p');
                    desc.textContent = p.descricao;
                    card.appendChild(desc);
                    const meta = document.createElement('p');
                    meta.className = 'tags';
                    meta.textContent = 'Categoria: ' + p.categoria + ' | Tecnologias: ' + (p.tecnologias || '—');
                    card.appendChild(meta);
                    grid.appendChild(card);
                });
            }
            if (select) {
                projetos.forEach(function (p) {
                    const o = document.createElement('option');
                    o.value = p.id_projeto;
                    o.textContent = p.titulo;
                    select.appendChild(o);
                });
            }
        });
    }
});
