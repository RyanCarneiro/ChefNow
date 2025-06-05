document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("formCadastro");
  const mensagem = document.getElementById("mensagem");

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const nome = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const cpf = document.getElementById("cpf").value;
    const nascimento = document.getElementById("nascimento").value;
    const cep = document.getElementById("cep").value;

    fetch("/cadastrar-chef", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        nome,
        email,
        password,
        cpf,
        nascimento,
        cep
      })
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        mensagem.innerText = data.msg;
        mensagem.style.color = "green";
        form.reset();
      } else {
        mensagem.innerText = data.msg;
        mensagem.style.color = "red";
      }
    })
    .catch(err => {
      console.error(err);
      mensagem.innerText = "Erro ao cadastrar.";
      mensagem.style.color = "red";
    });
  });
});
