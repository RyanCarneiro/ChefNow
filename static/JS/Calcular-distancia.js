// Seleciona o botão de busca por CEP e adiciona um event listener de clique
document.querySelector(".cep-button").addEventListener("click", async () => {
  // Seleciona o campo de input do CEP, obtém o valor e remove todos os não-dígitos
  const cepInput = document
    .querySelector(".cep-input")
    .value.replace(/\D/g, "");
  // Seleciona o elemento onde os resultados serão exibidos
  const resultadoLista = document.querySelector(".resultado");
  // Define um raio fixo de 150 para a busca de chefs próximos
  const raio = 150; // Raio fixo em números de CEPs

  // Valida se o CEP tem exatamente 8 dígitos
  if (cepInput.length !== 8) {
    // Exibe alerta se CEP for inválido e interrompe a execução
    alert("Digite um CEP válido com 8 dígitos.");
    return;
  }

  // Bloco try-catch para capturar erros durante a requisição
  try {
    // Faz requisição GET para o endpoint de busca de chefs próximos
    const response = await fetch(
      `http://localhost:5000/chefs-proximos?cep=${cepInput}&raio=${raio}`
    );
    // Converte a resposta para JSON de forma assíncrona
    const dados = await response.json();

    // Limpa o conteúdo anterior da lista de resultados
    resultadoLista.innerHTML = "";

    // Verifica se nenhum chef foi encontrado
    if (dados.length === 0) {
      // Exibe mensagem informando que nenhum chef foi encontrado
      resultadoLista.innerHTML = "<li>Nenhum chef encontrado nesse raio.</li>";
      // Interrompe a execução da função
      return;
    }

    // Itera sobre cada chef encontrado nos dados retornados
    dados.forEach((chef) => {
      // Cria um novo elemento de lista (li)
      const li = document.createElement("li");
      
      // Cria um elemento de link (a)
      const link = document.createElement("a");
      // Define o texto do link
      link.textContent = `Nome: ${chef.nome} | CEP: ${chef.cep}`;
      // Define href como "#" para funcionar como link
      
      
      
      // Adiciona event listener de clique ao link
      link.addEventListener("click", (e) => {
        e.preventDefault(); // Previne o comportamento padrão do link
        // Constrói a URL usando a base do Flask e parâmetros
        const url = new URL("/Perfil-chef", window.location.origin);
        // Redireciona para a página do perfil do chef
        window.location.href = url.toString();
        // Ou para abrir em nova aba:
      });
      
      // Adiciona o link ao elemento de lista
      li.appendChild(link);
      // Adiciona o elemento de lista ao container de resultados
      resultadoLista.appendChild(li);
    });
  // Captura qualquer erro que ocorra durante a requisição ou processamento
  } catch (error) {
    // Imprime o erro no console do navegador para debug
    console.error("Erro ao buscar chefs:", error);
    // Exibe alerta informando sobre o erro de conexão
    alert(
      "Erro ao conectar com o servidor. Verifique se o backend está rodando."
    );
  }
});