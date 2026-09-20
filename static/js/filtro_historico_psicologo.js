
const filtroModalidade = document.getElementById("filtroModalidade");

const consultas = document.querySelectorAll(".card-historico");


filtroModalidade.addEventListener("change", function () {

    const modalidadeSelecionada = this.value;


    consultas.forEach(function (consulta) {

        const modalidade = consulta.dataset.modalidade;


        if (
            modalidadeSelecionada === "" ||
            modalidade === modalidadeSelecionada
        ) {

            consulta.style.display = "block";

        } else {

            consulta.style.display = "none";

        }

    });

});
