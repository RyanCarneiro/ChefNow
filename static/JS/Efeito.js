// JavaScript para funcionalidade completa da página
// Aguarda o DOM estar completamente carregado antes de executar
document.addEventListener('DOMContentLoaded', function() {
    // ===== ELEMENTOS DO MENU LATERAL =====
    // Seleciona o elemento botão que abre o menu (hambúrguer)
    const menuToggle = document.getElementById('menu-toggle');
    // Seleciona o elemento da barra lateral (sidebar)
    const sidebar = document.getElementById('sidebar');
    // Seleciona o botão que fecha a sidebar
    const sidebarClose = document.getElementById('sidebar-close');

    // ===== ELEMENTOS DESKTOP =====
    // Botão do dropdown de tipo de usuário (versão desktop)
    const userTypeBtn = document.getElementById('userTypeBtn');
    // Container do dropdown de tipo de usuário (versão desktop)
    const userTypeDropdown = document.getElementById('userTypeDropdown');
    // Elemento que mostra o tipo selecionado (versão desktop)
    const selectedType = document.getElementById('selectedType');
    // Botão de criar conta (versão desktop)
    const createBtn = document.getElementById('createBtn');
    // Botão de login (versão desktop)
    const loginBtn = document.getElementById('loginBtn');
    
    // ===== ELEMENTOS MOBILE =====
    // Botão do dropdown de tipo de usuário (versão mobile)
    const userTypeBtnMobile = document.getElementById('userTypeBtnMobile');
    // Container do dropdown de tipo de usuário (versão mobile)
    const userTypeDropdownMobile = document.getElementById('userTypeDropdownMobile');
    // Elemento que mostra o tipo selecionado (versão mobile)
    const selectedTypeMobile = document.getElementById('selectedTypeMobile');
    // Botão de criar conta (versão mobile)
    const createBtnMobile = document.getElementById('createBtnMobile');
    // Botão de login (versão mobile)
    const loginBtnMobile = document.getElementById('loginBtnMobile');
    
    // ===== VARIÁVEL GLOBAL =====
    // Variável que armazena o tipo de usuário selecionado (padrão: 'usuário')
    let selectedUserType = 'usuário';
    
    // ===== FUNÇÕES =====
    
    // Função para fechar a sidebar
    function closeSidebar() {
        // Remove a classe 'active' da sidebar para escondê-la
        if (sidebar) {
            sidebar.classList.remove('active');
            // Restaura a barra de rolagem da página
            document.body.style.overflow = '';
        }
    }
    
    // Função para atualizar texto dos botões baseado no tipo de usuário selecionado
    function updateButtonTexts() {
        // Define o texto do botão criar conta baseado no tipo selecionado
        const createText = selectedUserType === 'chef' ? 'Criar Conta como Chef' : 'Criar Conta como Usuário';
        // Define o texto do botão login baseado no tipo selecionado
        const loginText = selectedUserType === 'chef' ? 'Entrar como Chef' : 'Entrar como Usuário';
        
        // Atualiza o texto do botão criar (desktop) se existir
        if (createBtn) createBtn.textContent = createText;
        // Atualiza o texto do botão login (desktop) se existir
        if (loginBtn) loginBtn.textContent = loginText;
        // Atualiza o texto do botão criar (mobile) se existir
        if (createBtnMobile) createBtnMobile.textContent = createText;
        // Atualiza o texto do botão login (mobile) se existir
        if (loginBtnMobile) loginBtnMobile.textContent = loginText;
    }
    
    // Função para redirecionar baseado no tipo de usuário selecionado
    function redirectToSignup() {
        // Se o tipo selecionado for 'chef'
        if (selectedUserType === 'chef') {
            // Redireciona para a página de cadastro de chef
            window.location.href = '/Cadastro-chef';
        } else {
            // Caso contrário, redireciona para a página de cadastro de usuário
            window.location.href = '/Criar-conta';
        }
    }
    
    // Função para redirecionar para login (você precisa implementar)
    function redirectToLogin() {
        if (selectedUserType === 'chef') {
            window.location.href = '/Login-chef'; // Ajuste conforme sua rota
        } else {
            window.location.href = '/Login'; // Ajuste conforme sua rota
        }
    }
    
    // Função para alternar a visibilidade do dropdown
    function toggleDropdown(btn, dropdown) {
        // Verifica se os elementos existem
        if (dropdown && btn) {
            // Alterna a classe 'show' no dropdown
            dropdown.classList.toggle('show');
            // Alterna a classe 'active' no botão
            btn.classList.toggle('active');
        }
    }
    
    // Função para selecionar um tipo de usuário
    function selectUserType(type, typeDisplay, dropdown, btn) {
        // Atualiza a variável global com o tipo selecionado
        selectedUserType = type;
        // Capitaliza a primeira letra do tipo para exibição
        const displayText = type.charAt(0).toUpperCase() + type.slice(1);
        
        // Atualiza o texto do elemento de exibição se existir
        if (typeDisplay) typeDisplay.textContent = displayText;
        // Atualiza o texto do elemento desktop se existir
        if (selectedType) selectedType.textContent = displayText;
        // Atualiza o texto do elemento mobile se existir
        if (selectedTypeMobile) selectedTypeMobile.textContent = displayText;
        
        // Atualizar opções selecionadas visualmente
        // Remove a classe 'selected' de todas as opções
        document.querySelectorAll('.user-type-option').forEach(opt => {
            opt.classList.remove('selected');
            // Adiciona a classe 'selected' apenas na opção atual
            if (opt.dataset.type === type) {
                opt.classList.add('selected');
            }
        });
        
        // Fecha o dropdown removendo a classe 'show'
        if (dropdown) dropdown.classList.remove('show');
        // Remove a classe 'active' do botão
        if (btn) btn.classList.remove('active');
        // Atualiza os textos dos botões
        updateButtonTexts();
    }
    
    // ===== EVENT LISTENERS PARA MENU LATERAL =====
    
    // Adiciona evento de clique no botão de toggle do menu
    if (menuToggle) {
        menuToggle.addEventListener('click', () => {
            // Adiciona a classe 'active' à sidebar para mostrar ela
            if (sidebar) {
                sidebar.classList.add('active');
                // Remove a barra de rolagem da página para evitar scroll duplo
                document.body.style.overflow = 'hidden';
            }
        });
    }
    
    // Adiciona evento de clique no botão de fechar sidebar
    if (sidebarClose) {
        sidebarClose.addEventListener('click', closeSidebar);
    }
    
    // ===== EVENT LISTENERS PARA BOTÕES DE CRIAR CONTA =====
    
    // Adiciona evento ao botão criar conta (desktop)
    if (createBtn) {
        createBtn.addEventListener('click', (e) => {
            // Previne o comportamento padrão do link/botão
            e.preventDefault();
            // Chama a função de redirecionamento
            redirectToSignup();
        });
    }
    
    // Adiciona evento ao botão criar conta (mobile)
    if (createBtnMobile) {
        createBtnMobile.addEventListener('click', (e) => {
            // Previne o comportamento padrão do link/botão
            e.preventDefault();
            // Chama a função de redirecionamento
            redirectToSignup();
        });
    }
    
    // ===== EVENT LISTENERS PARA BOTÕES DE LOGIN =====
    
    // Adiciona evento ao botão login (desktop)
    if (loginBtn) {
        loginBtn.addEventListener('click', (e) => {
            // Previne o comportamento padrão do link/botão
            e.preventDefault();
            // Chama função de redirecionamento para login
            redirectToLogin();
        });
    }
    
    // Adiciona evento ao botão login (mobile)
    if (loginBtnMobile) {
        loginBtnMobile.addEventListener('click', (e) => {
            // Previne o comportamento padrão do link/botão
            e.preventDefault();
            // Chama função de redirecionamento para login
            redirectToLogin();
        });
    }
    
    // ===== EVENT LISTENERS DESKTOP PARA DROPDOWN =====
    
    // Adiciona eventos ao dropdown desktop se existir
    if (userTypeBtn && userTypeDropdown) {
        // Evento de clique no botão do dropdown
        userTypeBtn.addEventListener('click', (e) => {
            // Para a propagação do evento (evita fechar imediatamente)
            e.stopPropagation();
            // Alterna a visibilidade do dropdown
            toggleDropdown(userTypeBtn, userTypeDropdown);
        });
        
        // Evento de clique dentro do dropdown
        userTypeDropdown.addEventListener('click', (e) => {
            // Verifica se o elemento clicado tem a classe 'user-type-option'
            if (e.target.classList.contains('user-type-option')) {
                // Seleciona o tipo de usuário baseado no data-type do elemento
                selectUserType(e.target.dataset.type, selectedType, userTypeDropdown, userTypeBtn);
            }
        });
    }
    
    // ===== EVENT LISTENERS MOBILE PARA DROPDOWN =====
    
    // Adiciona eventos ao dropdown mobile se existir
    if (userTypeBtnMobile && userTypeDropdownMobile) {
        // Evento de clique no botão do dropdown mobile
        userTypeBtnMobile.addEventListener('click', (e) => {
            // Para a propagação do evento (evita fechar imediatamente)
            e.stopPropagation();
            // Alterna a visibilidade do dropdown
            toggleDropdown(userTypeBtnMobile, userTypeDropdownMobile);
        });
        
        // Evento de clique dentro do dropdown mobile
        userTypeDropdownMobile.addEventListener('click', (e) => {
            // Verifica se o elemento clicado tem a classe 'user-type-option'
            if (e.target.classList.contains('user-type-option')) {
                // Seleciona o tipo de usuário baseado no data-type do elemento
                selectUserType(e.target.dataset.type, selectedTypeMobile, userTypeDropdownMobile, userTypeBtnMobile);
            }
        });
    }
    
    // ===== EVENT LISTENERS GLOBAIS =====
    
    // Fechar sidebar ao clicar fora
    document.addEventListener('click', (e) => {
        // Verifica se a sidebar existe, está ativa, e o clique foi fora dela e do botão toggle
        if (sidebar && sidebar.classList.contains('active') && 
            !sidebar.contains(e.target) && 
            menuToggle && !menuToggle.contains(e.target)) {
            // Remove a classe 'active' para fechar a sidebar
            closeSidebar();
        }
    });
    
    // Fechar dropdown ao clicar fora
    document.addEventListener('click', () => {
        // Fecha dropdown desktop se existir
        if (userTypeDropdown) {
            userTypeDropdown.classList.remove('show');
            // Remove classe 'active' do botão desktop
            if (userTypeBtn) userTypeBtn.classList.remove('active');
        }
        // Fecha dropdown mobile se existir
        if (userTypeDropdownMobile) {
            userTypeDropdownMobile.classList.remove('show');
            // Remove classe 'active' do botão mobile
            if (userTypeBtnMobile) userTypeBtnMobile.classList.remove('active');
        }
    });
    
    // ===== INICIALIZAÇÃO =====
    
    // Inicializar texto dos botões
    updateButtonTexts();
    
// Fecha a função DOMContentLoaded
});