// ============================
// PARTE 1: VARIÁVEL GLOBAL
// ============================

// Esta variável guarda qual tipo de usuário está tentando fazer login
// Por padrão, assume que é um cliente
let currentUserType = 'cliente';

// ============================
// PARTE 2: SELETOR DE TIPO DE USUÁRIO
// ============================

// Pega todos os botões que têm a classe 'user-type-btn' (botões de Cliente/Chef)
document.querySelectorAll('.user-type-btn').forEach(btn => {
    // Para cada botão, adiciona um evento de clique
    btn.addEventListener('click', function () {
        // Remove a classe 'active' de TODOS os botões (limpa seleção anterior)
        document.querySelectorAll('.user-type-btn').forEach(b => b.classList.remove('active'));
        
        // Adiciona a classe 'active' apenas no botão clicado (marca como selecionado)
        this.classList.add('active');
        
        // Pega o tipo do usuário do atributo data-type do botão clicado
        // Exemplo: <button data-type="chef">Chef</button>
        currentUserType = this.dataset.type;
    });
});

// ============================
// PARTE 3: SISTEMA DE ALERTAS
// ============================

// Função para mostrar mensagens na tela (erro, sucesso, etc.)
function showAlert(message, type = 'error') {
    // Pega o elemento HTML onde a mensagem será exibida
    const alert = document.getElementById('alert');
    
    // Define a classe CSS baseada no tipo (alert-error, alert-success, etc.)
    alert.className = `alert alert-${type}`;
    
    // Coloca o texto da mensagem dentro do elemento
    alert.textContent = message;
    
    // Adiciona a classe 'show' para tornar o alerta visível
    alert.classList.add('show');

    // Após 5 segundos (5000ms), remove o alerta da tela
    setTimeout(() => {
        alert.classList.remove('show');
    }, 5000);
}

// ============================
// PARTE 4: GERENCIAMENTO DE TOKEN
// ============================

// Função para SALVAR o token de autenticação no navegador
function setAuthToken(token) {
    // localStorage é como um "cofre" no navegador que guarda dados
    localStorage.setItem('authToken', token);
}

// Função para RECUPERAR o token salvo
function getAuthToken() {
    // Busca o token que foi salvo anteriormente
    return localStorage.getItem('authToken');
}

// Função para REMOVER o token (usado quando o usuário faz logout)
function removeAuthToken() {
    localStorage.removeItem('authToken');
}

// ============================
// PARTE 5: REQUISIÇÕES COM AUTENTICAÇÃO
// ============================

// Função que facilita fazer requisições para o servidor incluindo o token
function fetchWithAuth(url, options = {}) {
    // Pega o token salvo
    const token = getAuthToken();
    
    // Se existe um token...
    if (token) {
        // Adiciona o token no cabeçalho da requisição
        options.headers = {
            ...options.headers, // Mantém outros cabeçalhos que já existiam
            'Authorization': `Bearer ${token}` // Adiciona o token de autorização
        };
    }
    
    // Faz a requisição normal, mas agora com o token incluído
    return fetch(url, options);
}

// ============================
// PARTE 6: VERIFICAÇÃO DE LOGIN
// ============================

// Função que verifica se o usuário já está logado
function checkAuthStatus() {
    // Pega o token salvo
    const token = getAuthToken();
    
    // Se existe um token...
    if (token) {
        // Pergunta para o servidor se este token ainda é válido
        fetchWithAuth('/api/verificar-token')
            .then(response => response.json()) // Converte resposta para JSON
            .then(data => {
                // Se o servidor disse que o token é válido...
                if (data.success) {
                    // Usuário já está logado! Redireciona para a página dele
                    redirectAfterLogin(data.user.tipo);
                } else {
                    // Token é inválido (expirou, foi alterado, etc.)
                    // Remove o token "estragado"
                    removeAuthToken();
                }
            })
            .catch(error => {
                // Se deu erro ao verificar (sem internet, servidor fora do ar, etc.)
                console.error('Erro ao verificar token:', error);
                removeAuthToken(); // Remove o token por segurança
            });
    }
}

// ============================
// PARTE 7: REDIRECIONAMENTO
// ============================

// Função que leva o usuário para a página certa depois do login
function redirectAfterLogin(userType) {
    if (userType === 'chef') {
        // Se é um chef, vai para a página do perfil do chef
        window.location.href = '/Perfil-chef';
    } else {
        // Se é cliente (ou qualquer outro tipo), vai para a página inicial
        window.location.href = '/';
    }
}

// ============================
// PARTE 8: PROCESSAMENTO DO FORMULÁRIO DE LOGIN
// ============================

// Pega o formulário de login e adiciona um evento para quando for enviado
document.getElementById('loginForm').addEventListener('submit', async function (e) {
    // Impede que a página recarregue (comportamento padrão de formulário)
    e.preventDefault();

    // Pega os valores que o usuário digitou
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    // Pega referências dos elementos da interface
    const loginBtn = document.getElementById('loginBtn');
    const loading = document.getElementById('loading');

    // Verifica se o usuário preencheu os campos
    if (!email || !password) {
        showAlert('Por favor, preencha todos os campos!');
        return; // Para a execução da função
    }

    // ============================
    // INÍCIO DO PROCESSO DE LOGIN
    // ============================
    
    // Desabilita o botão para evitar cliques múltiplos
    loginBtn.disabled = true;
    // Mostra o indicador de carregamento
    loading.style.display = 'block';

    try {
        // Envia os dados para o servidor
        const response = await fetch('/api/login', {
            method: 'POST', // Método HTTP POST
            headers: {
                'Content-Type': 'application/json', // Diz que está enviando JSON
            },
            body: JSON.stringify({ // Converte objeto para JSON
                email: email,
                password: password,
                tipo: currentUserType // Envia se é cliente ou chef
            })
        });

        // Converte a resposta do servidor para JavaScript
        const data = await response.json();

        // Se o login deu certo...
        if (data.success) {
            // Salva o token que o servidor enviou
            setAuthToken(data.token);

            // Mostra mensagem de sucesso
            showAlert('Login realizado com sucesso!', 'success');

            // Espera 1 segundo e depois redireciona
            setTimeout(() => {
                redirectAfterLogin(data.user.tipo);
            }, 1000);
        } else {
            // Se deu erro (senha errada, usuário não existe, etc.)
            showAlert(data.msg || 'Erro ao fazer login');
        }
    } catch (error) {
        // Se deu erro na comunicação (sem internet, servidor fora do ar, etc.)
        console.error('Erro no login:', error);
        showAlert('Erro de conexão. Tente novamente.');
    } finally {
        // SEMPRE executa, deu certo ou não
        // Reabilita o botão e esconde o loading
        loginBtn.disabled = false;
        loading.style.display = 'none';
    }
});

// ============================
// PARTE 9: INICIALIZAÇÃO
// ============================

// Quando a página terminar de carregar completamente...
document.addEventListener('DOMContentLoaded', function () {
    // Verifica se o usuário já está logado
    checkAuthStatus();
});

// ============================
// PARTE 10: FUNÇÃO DE LOGOUT
// ============================

// Função para fazer logout (pode ser chamada de outras páginas)
function logout() {
    removeAuthToken(); // Remove o token salvo
    window.location.href = "/login" // Volta para a página de login
}