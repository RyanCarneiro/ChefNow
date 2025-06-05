document.querySelector(".cep-button").addEventListener("click", async () => {
  const cepInput = document
    .querySelector(".cep-input")
    .value.replace(/\D/g, "");
  const resultadoLista = document.querySelector(".resultado");
  const raio = 50; // Raio fixo em números de CEPs

  if (cepInput.length !== 8) {
    alert("Digite um CEP válido com 8 dígitos.");
    return;
  }

  try {
    const response = await fetch(
      `http://localhost:5000/chefs-proximos?cep=${cepInput}&raio=${raio}`
    );
    const dados = await response.json();

    resultadoLista.innerHTML = "";

    if (dados.length === 0) {
      resultadoLista.innerHTML = "<li>Nenhum chef encontrado nesse raio.</li>";
      return;
    }

    dados.forEach((chef) => {
      const li = document.createElement("li");
      li.textContent = `Nome: ${chef.nome} | CEP: ${chef.cep} `;
      resultadoLista.appendChild(li);
    });
  } catch (error) {
    console.error("Erro ao buscar chefs:", error);
    alert(
      "Erro ao conectar com o servidor. Verifique se o backend está rodando."
    );
  }
});
