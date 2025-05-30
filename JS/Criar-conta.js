document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("formCadastro");

    form.addEventListener("submit", function (e) {
        e.preventDefault();
        const nome = document.getElementById("name").value;
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;
        const cpf = document.getElementById("cpf").value;
        const nascimento = document.getElementById("nascimento").value;

        fetch("/cadastrar", {
            method: "POST",
            body: `nome=${encodeURIComponent(nome)}&email${encodeURIComponent(email)}&senha${encodeURIComponent(password)}&cpf=${encodeURIComponent(cpf)}&nascimento${encodeURIComponent(nascimento)}`,
            body: JSON.stringify(FormData),
        })
            .then((res) => res.text())
            .catch((err) => {
                console.error(err);
                mensagem.innerText = "ERRO ao cadastrar"
            });
    })

})
