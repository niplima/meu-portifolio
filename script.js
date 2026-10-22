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

    // === 2. FORMULÁRIO DE CONTATO INTERATIVO (Página Contato) ===
    const formContato = document.querySelector('form');
    const mensagemFeedback = document.querySelector('#feedback-mensagem');

    if (formContato) {
        formContato.addEventListener('submit', function (event) {
            const nomeInput = document.querySelector('#nome');
            const nome = nomeInput ? nomeInput.value : 'Usuário';

            if (mensagemFeedback) {
                mensagemFeedback.textContent = `Obrigado, ${nome}! Sua mensagem foi enviada com sucesso.`;
                mensagemFeedback.classList.add('sucesso');
                mensagemFeedback.style.display = 'block';
            }

        });
    }
});