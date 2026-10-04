// Altura (em pixels) que o texto tem quando está recolhido.
const ALTURA_MAXIMA = 110;

// Espera a página (e as fontes) carregarem, para medir o texto corretamente.
window.addEventListener("load", function () {

    const cards = document.querySelectorAll(".card-dica");

    cards.forEach(function (card) {

        const texto = card.querySelector(".card-dica-texto");
        const botao = card.querySelector(".btn-ler-mais");

        // Texto curto: cabe inteiro, então não precisa de "ler mais".
        if (texto.scrollHeight <= ALTURA_MAXIMA) {
            return;
        }

        // Texto longo: recolhe, aplica o sombreado e mostra o botão.
        texto.classList.add("recolhido");
        texto.style.maxHeight = ALTURA_MAXIMA + "px";
        botao.hidden = false;

        botao.addEventListener("click", function () {

            const estaRecolhido = texto.classList.contains("recolhido");

            if (estaRecolhido) {
                texto.classList.remove("recolhido");
                texto.style.maxHeight = texto.scrollHeight + "px";
                botao.innerHTML = 'Ler menos <i class="fa-solid fa-chevron-up"></i>';
            } else {
                texto.classList.add("recolhido");
                texto.style.maxHeight = ALTURA_MAXIMA + "px";
                botao.innerHTML = 'Ler mais <i class="fa-solid fa-chevron-down"></i>';
            }
        });
    });
});