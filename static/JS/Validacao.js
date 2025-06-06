// Aguarda o carregamento completo da página antes de executar o código
document.addEventListener('DOMContentLoaded', function () {

    // Obtém referências para todos os elementos do SEU formulário (IDs originais mantidos)
    const form = document.getElementById('formCadastro'); // Seu ID original
    const nameInput = document.getElementById('name');     // Seu ID original
    const emailInput = document.getElementById('email');   // Seu ID original
    const passwordInput = document.getElementById('password'); // Seu ID original
    const cpfInput = document.getElementById('cpf');       // Seu ID original
    const nascimentoInput = document.getElementById('nascimento'); // Seu ID original
    const cepInput = document.getElementById('cep');       // Seu ID original

    // VALIDAÇÃO DO CAMPO NOME
    // Executa validação sempre que o usuário digita algo no campo nome
    nameInput.addEventListener('input', function () {
        const value = this.value.trim(); // Obtém o valor digitado e remove espaços extras
        const errorElement = document.getElementById('name-error'); // Elemento para mostrar erro
        const successElement = document.getElementById('name-success'); // Elemento para mostrar sucesso

        // Verifica se o nome tem pelo menos 2 caracteres
        if (value.length < 2) {
            showError(this, errorElement, successElement, 'Nome deve ter pelo menos 2 caracteres');
        }
        // Verifica se o nome contém apenas letras e espaços (sem números ou símbolos)
        else if (!/^[a-zA-ZÀ-ÿ\s]+$/.test(value)) {
            showError(this, errorElement, successElement, 'Nome deve conter apenas letras');
        }
        // Se passou em todas as validações, marca como válido
        else {
            showSuccess(this, errorElement, successElement, 'Nome válido');
        }
    });

    // VALIDAÇÃO DO CAMPO EMAIL
    // Executa validação sempre que o usuário digita algo no campo email
    emailInput.addEventListener('input', function () {
        const value = this.value.trim(); // Obtém o valor e remove espaços
        const errorElement = document.getElementById('email-error');
        const successElement = document.getElementById('email-success');

        // Expressão regular para validar formato de email (mais rigorosa que o HTML5)
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        // Verifica se o email está no formato correto
        if (!emailRegex.test(value)) {
            showError(this, errorElement, successElement, 'Digite um email válido');
        } else {
            showSuccess(this, errorElement, successElement, 'Email válido');
        }
    });

    // VALIDAÇÃO DO CAMPO SENHA
    // Executa validação sempre que o usuário digita algo no campo senha
    passwordInput.addEventListener('input', function () {
        const value = this.value; // Obtém o valor da senha
        const errorElement = document.getElementById('password-error');
        const successElement = document.getElementById('password-success');

        // Verifica se a senha tem pelo menos 8 caracteres
        if (value.length < 8) {
            showError(this, errorElement, successElement, 'Senha deve ter pelo menos 8 caracteres');
        }
        // Verifica se a senha tem pelo menos: 1 maiúscula, 1 minúscula e 1 número
        else if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(value)) {
            showError(this, errorElement, successElement, 'Senha deve ter ao menos: 1 maiúscula, 1 minúscula e 1 número');
        }
        // Se passou em todas as validações, marca como forte
        else {
            showSuccess(this, errorElement, successElement, 'Senha forte');
        }
    });

    // VALIDAÇÃO E MÁSCARA DO CAMPO CPF
    // Executa sempre que o usuário digita algo no campo CPF
    cpfInput.addEventListener('input', function () {
        let value = this.value; // Obtém o valor atual

        // Remove todos os caracteres que não são números
        value = value.replace(/\D/g, '');

        // Limita o CPF a no máximo 11 dígitos
        if (value.length > 11) {
            value = value.substring(0, 11);
        }

        // Aplica a máscara do CPF no formato XXX.XXX.XXX-XX
        if (value.length > 3) {
            value = value.substring(0, 3) + '.' + value.substring(3);
        }
        if (value.length > 7) {
            value = value.substring(0, 7) + '.' + value.substring(7);
        }
        if (value.length > 11) {
            value = value.substring(0, 11) + '-' + value.substring(11);
        }

        // Atualiza o valor do campo com a máscara aplicada
        this.value = value;

        // Validação do CPF
        const errorElement = document.getElementById('cpf-error');
        const successElement = document.getElementById('cpf-success');
        const cleanCpf = value.replace(/\D/g, ''); // Remove pontos e traços para validação

        // Verifica se o CPF tem exatamente 11 dígitos
        if (cleanCpf.length !== 11) {
            showError(this, errorElement, successElement, 'CPF deve ter 11 dígitos');
        }
        // Verifica se o CPF é matematicamente válido usando o algoritmo oficial
        else if (!isValidCPF(cleanCpf)) {
            showError(this, errorElement, successElement, 'CPF inválido');
        }
        // Se passou em todas as validações, marca como válido
        else {
            showSuccess(this, errorElement, successElement, 'CPF válido');
        }
    });

    // VALIDAÇÃO E MÁSCARA DO CAMPO CEP
    // Executa sempre que o usuário digita algo no campo CEP
    cepInput.addEventListener('input', function () {
        let value = this.value; // Obtém o valor atual

        // Remove todos os caracteres que não são números (RESOLVE O PROBLEMA DE LETRAS)
        value = value.replace(/\D/g, '');

        // Limita o CEP a no máximo 8 dígitos (RESOLVE O PROBLEMA DE TAMANHO)
        if (value.length > 8) {
            value = value.substring(0, 8);
        }

        // Aplica a máscara do CEP no formato XXXXX-XXX
        if (value.length > 5) {
            value = value.substring(0, 5) + '-' + value.substring(5);
        }

        // Atualiza o valor do campo com a máscara aplicada
        this.value = value;

        // Validação do CEP
        const errorElement = document.getElementById('cep-error');
        const successElement = document.getElementById('cep-success');
        const cleanCep = value.replace(/\D/g, ''); // Remove o traço para validação

        // Verifica se o CEP tem exatamente 8 dígitos
        if (cleanCep.length !== 8) {
            showError(this, errorElement, successElement, 'CEP deve ter 8 dígitos');
        } else {
            showSuccess(this, errorElement, successElement, 'CEP válido');
        }
    });

    // VALIDAÇÃO DO CAMPO DATA DE NASCIMENTO
    // Executa sempre que o usuário seleciona/altera a data
    nascimentoInput.addEventListener('input', function () {
        const value = this.value; // Obtém a data selecionada
        const errorElement = document.getElementById('nascimento-error');
        const successElement = document.getElementById('nascimento-success');

        // Verifica se uma data foi selecionada
        if (!value) {
            showError(this, errorElement, successElement, 'Data de nascimento é obrigatória');
            return;
        }

        // Converte a data selecionada e a data atual para objetos Date
        const birthDate = new Date(value);
        const today = new Date();

        // Calcula a idade
        const age = today.getFullYear() - birthDate.getFullYear();
        const monthDiff = today.getMonth() - birthDate.getMonth();

        // Ajusta a idade se ainda não fez aniversário este ano
        const finalAge = monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate()) ? age - 1 : age;

        // Verifica se a data não é no futuro
        if (birthDate > today) {
            showError(this, errorElement, successElement, 'Data não pode ser no futuro');
        }
        // Verifica se a pessoa tem pelo menos 16 anos
        else if (finalAge < 16) {
            showError(this, errorElement, successElement, 'Idade mínima: 16 anos');
        }
        // Verifica se a idade é realista (máximo 120 anos)
        else if (finalAge > 120) {
            showError(this, errorElement, successElement, 'Data de nascimento inválida');
        }
        // Se passou em todas as validações, marca como válida
        else {
            showSuccess(this, errorElement, successElement, 'Data válida');
        }
    });

    // FUNÇÃO PARA VALIDAR CPF USANDO O ALGORITMO OFICIAL BRASILEIRO
    // Esta função implementa o cálculo matemático real usado para validar CPFs
    function isValidCPF(cpf) {
        // Elimina CPFs com todos os dígitos iguais (ex: 111.111.111-11)
        if (/^(\d)\1{10}$/.test(cpf)) return false;

        // Calcula o primeiro dígito verificador
        let sum = 0;
        for (let i = 0; i < 9; i++) {
            sum += parseInt(cpf.charAt(i)) * (10 - i);
        }
        let digit1 = 11 - (sum % 11);
        if (digit1 > 9) digit1 = 0;

        // Calcula o segundo dígito verificador
        sum = 0;
        for (let i = 0; i < 10; i++) {
            sum += parseInt(cpf.charAt(i)) * (11 - i);
        }
        let digit2 = 11 - (sum % 11);
        if (digit2 > 9) digit2 = 0;

        // Verifica se os dígitos calculados conferem com os informados no CPF
        return digit1 === parseInt(cpf.charAt(9)) && digit2 === parseInt(cpf.charAt(10));
    }

    // FUNÇÃO PARA MOSTRAR ERRO EM UM CAMPO
    // Adiciona classe de erro, mostra mensagem de erro e esconde mensagem de sucesso
    function showError(input, errorElement, successElement, message) {
        input.classList.remove('valid');   // Remove classe de válido
        input.classList.add('error');      // Adiciona classe de erro (borda vermelha)
        errorElement.textContent = message; // Define o texto da mensagem de erro
        errorElement.style.display = 'block'; // Mostra a mensagem de erro
        successElement.style.display = 'none'; // Esconde a mensagem de sucesso
    }

    // FUNÇÃO PARA MOSTRAR SUCESSO EM UM CAMPO
    // Adiciona classe de válido, mostra mensagem de sucesso e esconde mensagem de erro
    function showSuccess(input, errorElement, successElement, message) {
        input.classList.remove('error');   // Remove classe de erro
        input.classList.add('valid');      // Adiciona classe de válido (borda verde)
        successElement.textContent = message; // Define o texto da mensagem de sucesso
        successElement.style.display = 'block'; // Mostra a mensagem de sucesso
        errorElement.style.display = 'none'; // Esconde a mensagem de erro
    }

    // VALIDAÇÃO FINAL NO ENVIO DO FORMULÁRIO
    // Executa quando o usuário clica no botão "Cadastrar"
    form.addEventListener('submit', function (e) {
        e.preventDefault(); // Impede o envio padrão do formulário para fazer validação final

        // Conta quantos campos estão válidos e quantos campos são obrigatórios
        const validFields = document.querySelectorAll('input.valid');
        const totalFields = document.querySelectorAll('input[required]');

        // Se todos os campos obrigatórios estão válidos, permite o envio
        if (validFields.length === totalFields.length) {
            alert('Formulário enviado com sucesso!');
            // AQUI VOCÊ PODE ADICIONAR O CÓDIGO PARA ENVIAR OS DADOS PARA SEU SERVIDOR
            console.log('Dados do formulário:', new FormData(form));
        }
        // Se ainda há campos inválidos, mostra mensagem de erro
        else {
            alert('Por favor, corrija os erros antes de enviar o formulário.');
        }
    });

}); // Fim do DOMContentLoaded