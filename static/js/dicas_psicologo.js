const ALTURA_MAXIMA = 110;

window.addEventListener("load", function () {

    const cards = document.querySelectorAll(".card-dica");

    cards.forEach(function (card) {

        const texto = card.querySelector(".card-dica-texto");
        const botao = card.querySelector(".btn-ler-mais");

        if (texto.scrollHeight <= ALTURA_MAXIMA) {
            return;
        }

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

    const modal = document.getElementById("modalDica");

    if (!modal) {
        return;
    }

    const modalTitulo = document.getElementById("modalDicaTitulo");
    const inputId = document.getElementById("inputIdDica");
    const inputTitulo = document.getElementById("inputTituloDica");
    const inputTexto = document.getElementById("inputTextoDica");
    const btnNovaDica = document.getElementById("btnNovaDica");
    const btnFecharModal = document.getElementById("btnFecharModalDica");

    function abrirModal() {
        modal.hidden = false;
    }

    function fecharModal() {
        modal.hidden = true;
    }

    if (btnNovaDica) {
        btnNovaDica.addEventListener("click", function () {
            modalTitulo.innerHTML = '<i class="fa-solid fa-lightbulb"></i> Nova dica';
            inputId.value = "";
            inputTitulo.value = "";
            inputTexto.value = "";
            abrirModal();
        });
    }

    document.querySelectorAll(".btn-editar-dica").forEach(function (botaoEditar) {
        botaoEditar.addEventListener("click", function () {
            modalTitulo.innerHTML = '<i class="fa-solid fa-pen"></i> Editar dica';
            inputId.value = botaoEditar.dataset.id;
            inputTitulo.value = botaoEditar.dataset.titulo;
            inputTexto.value = botaoEditar.dataset.texto;
            abrirModal();
        });
    });

    if (btnFecharModal) {
        btnFecharModal.addEventListener("click", fecharModal);
    }

    modal.addEventListener("click", function (evento) {
        if (evento.target === modal) {
            fecharModal();
        }
    });

    document.addEventListener("keydown", function (evento) {
        if (evento.key === "Escape" && !modal.hidden) {
            fecharModal();
        }
    });
});