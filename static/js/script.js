const btnDesigner = document.getElementById("btnDesigner");
const btnGestor = document.getElementById("btnGestor");
const paletaForm = document.getElementById("paletaForm");
const anuncioForm = document.getElementById("anuncioForm");
const gerarPaletaBtn = document.getElementById("gerarPaleta");
const descricaoCores = document.getElementById("descricaoCores");
const resultadoPaleta = document.getElementById("resultadoPaleta");
const novaPaletaBtn = document.getElementById("novaPaleta");

const addCampanhaBtn = document.getElementById("addCampanhaBtn");
const campanhasContainer = document.getElementById("campanhasContainer");
const iniciarAnaliseBtn = document.getElementById("iniciarAnalise");
const metaCliquesInput = document.getElementById("metaCliques");
const metaConversoesInput = document.getElementById("metaConversoes");
const resultadoAnalise = document.getElementById("resultadoAnalise");
const numCampanhasInput = document.getElementById("numCampanhas"); // Adicionado

btnDesigner.addEventListener("click", () => {
    paletaForm.classList.remove("hidden");
    anuncioForm.classList.add("hidden");
    resultadoPaleta.innerHTML = ""; // limpa resultados anteriores
    descricaoCores.value = ""; // limpa descrição
});

btnGestor.addEventListener("click", () => {
    anuncioForm.classList.remove("hidden");
    paletaForm.classList.add("hidden");
    resultadoAnalise.innerHTML = ""; // limpa resultados anteriores
    numCampanhasInput.value = ""; // limpa número de campanhas
});

// Função para gerar paleta de cores
gerarPaletaBtn.addEventListener("click", () => {
    const descricao = descricaoCores.value;
    if (descricao) {
        fetch("/gerar_paleta", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ descricao: descricao })
        })
        .then(response => response.json())
        .then(data => {
            if (data.paleta) {
                resultadoPaleta.innerHTML = `<p>Paleta gerada:</p>`;
                data.paleta.forEach(cor => {
                    resultadoPaleta.innerHTML += `<div style="background-color: ${cor}; width: 50px; height: 50px; display: inline-block; margin: 2px;"></div>`;
                });
                novaPaletaBtn.classList.remove("hidden");
            } else if (data.error) {
                resultadoPaleta.innerHTML = `<p>${data.error}</p>`;
            }
        })
        .catch(error => {
            console.error("Erro ao gerar paleta:", error);
            resultadoPaleta.innerHTML = "<p>Erro ao gerar paleta. Tente novamente.</p>";
        });
    }
});

// Botão para gerar uma nova paleta
novaPaletaBtn.addEventListener("click", () => {
    resultadoPaleta.innerHTML = "";
    novaPaletaBtn.classList.add("hidden");
});

// Adicionar campos de entrada para cada campanha
addCampanhaBtn.addEventListener("click", () => {
    const campanhaIndex = campanhasContainer.children.length + 1;

    // Cria uma div para a nova campanha
    const campanhaDiv = document.createElement("div");
    campanhaDiv.classList.add("campanha");
    campanhaDiv.innerHTML = `
        <h3>Campanha ${campanhaIndex}</h3>
        <input type="number" placeholder="Gastos (em R$)" class="gastos">
        <input type="number" placeholder="Cliques" class="cliques">
        <input type="number" placeholder="Impressões" class="impressoes">
        <input type="number" placeholder="Conversões" class="conversoes">
        <input type="number" placeholder="CPA (Custo por Aquisição)" class="cpa">
        <input type="text" placeholder="Público-alvo" class="publico_alvo">
        <input type="text" placeholder="Horário" class="horario">
        <input type="text" placeholder="Dia da semana" class="dia_da_semana">
        <input type="text" placeholder="Plataforma" class="plataforma">
        <input type="text" placeholder="Dispositivo" class="dispositivo">
    `;
    campanhasContainer.appendChild(campanhaDiv);
});

// Enviar dados das campanhas para análise
iniciarAnaliseBtn.addEventListener("click", () => {
    const numCampanhas = parseInt(numCampanhasInput.value);
    const metaCliques = parseInt(metaCliquesInput.value);
    const metaConversoes = parseInt(metaConversoesInput.value);

    // Coletar dados de cada campanha
    const campanhas = Array.from(campanhasContainer.children).map(campanhaDiv => ({
        gastos: parseFloat(campanhaDiv.querySelector(".gastos").value),
        cliques: parseInt(campanhaDiv.querySelector(".cliques").value),
        impressoes: parseInt(campanhaDiv.querySelector(".impressoes").value),
        conversoes: parseInt(campanhaDiv.querySelector(".conversoes").value),
        cpa: parseFloat(campanhaDiv.querySelector(".cpa").value),
        publico_alvo: campanhaDiv.querySelector(".publico_alvo").value,
        horario: campanhaDiv.querySelector(".horario").value,
        dia_da_semana: campanhaDiv.querySelector(".dia_da_semana").value,
        plataforma: campanhaDiv.querySelector(".plataforma").value,
        dispositivo: campanhaDiv.querySelector(".dispositivo").value,
    }));

    if (campanhas.length && metaCliques && metaConversoes) {
        fetch("/analisar_anuncios", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                numCampanhas: numCampanhas, // Adicionado para o AdOptimizer
                campanhas: campanhas,
                metaCliques: metaCliques,
                metaConversoes: metaConversoes
            })
        })
        .then(response => response.json())
        .then(data => {
            resultadoAnalise.innerHTML = `<p>Resultado da análise:</p>`;
            resultadoAnalise.innerHTML += `<p>Cliques recomendados: ${data.recomendacaoCliques}</p>`;
            resultadoAnalise.innerHTML += `<p>Conversões recomendadas: ${data.recomendacaoConversoes}</p>`;
        })
        .catch(error => {
            console.error("Erro ao analisar campanhas:", error);
            resultadoAnalise.innerHTML = "<p>Erro ao analisar campanhas. Tente novamente.</p>";
        });
    } else {
        alert("Por favor, preencha todos os campos e adicione pelo menos uma campanha.");
    }
});
