// Aguarda o DOM estar completamente carregado antes de executar o código
document.addEventListener("DOMContentLoaded", () => {
  // Seleciona o elemento do formulário de cadastro pelo ID
  const form = document.getElementById("formCadastro");
  // Seleciona o elemento onde as mensagens serão exibidas pelo ID
  const mensagem = document.getElementById("mensagem");

  // Adiciona um event listener para o evento de submit do formulário
  form.addEventListener("submit", function (e) {
    // Previne o comportamento padrão do formulário (evita recarregar a página)
    e.preventDefault();

    // Obtém o valor do campo nome pelo ID
    const nome = document.getElementById("name").value;
    // Obtém o valor do campo email pelo ID
    const email = document.getElementById("email").value;
    // Obtém o valor do campo password pelo ID
    const password = document.getElementById("password").value;
    // Obtém o valor do campo cpf pelo ID
    const cpf = document.getElementById("cpf").value;
    // Obtém o valor do campo nascimento pelo ID
    const nascimento = document.getElementById("nascimento").value;
    // Obtém o valor do campo cep pelo ID
    const cep = document.getElementById("cep").value;

    // Faz uma requisição HTTP POST para o endpoint do servidor
    fetch("/cadastrar-chef", {
      // Define o método HTTP como POST
      method: "POST",
      // Define os cabeçalhos da requisição
      headers: {
        // Especifica que o conteúdo enviado será JSON
        "Content-Type": "application/json"
      },
      // Converte o objeto JavaScript em string JSON para envio
      body: JSON.stringify({
        nome,       // Equivale a nome: nome
        email,      // Equivale a email: email
        password,   // Equivale a password: password
        cpf,        // Equivale a cpf: cpf
        nascimento, // Equivale a nascimento: nascimento
        cep         // Equivale a cep: cep
      })
    })
    // Converte a resposta da requisição para JSON
    .then(res => res.json())
    // Processa os dados da resposta JSON
    .then(data => {
      // Verifica se o cadastro foi bem-sucedido
      if (data.success) {
        // Define o texto da mensagem com a resposta do servidor
        mensagem.innerText = data.msg;
        // Define a cor da mensagem como verde (sucesso)
        mensagem.style.color = "green";
        // Limpa todos os campos do formulário
        form.reset();
      } else {
        // Define o texto da mensagem com o erro do servidor
        mensagem.innerText = data.msg;
        // Define a cor da mensagem como vermelho (erro)
        mensagem.style.color = "red";
      }
    })
    // Captura erros que possam ocorrer durante a requisição
    .catch(err => {
      // Imprime o erro no console do navegador para debug
      console.error(err);
      // Exibe mensagem genérica de erro para o usuário
      mensagem.innerText = "Erro ao cadastrar.";
      // Define a cor da mensagem como vermelho (erro)
      mensagem.style.color = "red";
    });
  });
// Fecha a função do event listener DOMContentLoaded
});