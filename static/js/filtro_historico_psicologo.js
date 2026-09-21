
const filtroModalidade = document.getElementById("filtroModalidade");
const filtroNome = document.getElementById("filtroNome");
const semResultado = document.getElementById("semResultadoHistorico");

const consultas = document.querySelectorAll(".card-historico");


function aplicarFiltros() {

    const modalidadeSelecionada = filtroModalidade.value;
    const nomeDigitado = filtroNome.value.trim().toLowerCase();

    let algumVisivel = false;

    consultas.forEach(function (consulta) {

        const modalidade = consulta.dataset.modalidade;
        const nomeAluno = (consulta.dataset.nome || "").toLowerCase();

        const combinaModalidade =
            modalidadeSelecionada === "" ||
            modalidade === modalidadeSelecionada;

        const combinaNome =
            nomeDigitado === "" ||
            nomeAluno.indexOf(nomeDigitado) > -1;

        if (combinaModalidade && combinaNome) {
            consulta.style.display = "block";
            algumVisivel = true;
        } else {
            consulta.style.display = "none";
        }

    });

    semResultado.style.display = algumVisivel ? "none" : "block";
}


filtroModalidade.addEventListener("change", aplicarFiltros);
filtroNome.addEventListener("input", aplicarFiltros);
