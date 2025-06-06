// JavaScript para funcionalidade do menu lateral
const menuToggle = document.getElementById('menu-toggle');
const sidebar = document.getElementById('sidebar');
const sidebarClose = document.getElementById('sidebar-close');

menuToggle.addEventListener('click', () => {
    sidebar.classList.add('active');
    document.body.style.overflow = 'hidden';
});

function closeSidebar() {
    sidebar.classList.remove('active');
    document.body.style.overflow = '';
}

sidebarClose.addEventListener('click', closeSidebar);

// JavaScript para funcionalidade de seleção de tipo de usuário e redirecionamento
document.addEventListener('DOMContentLoaded', function() {
    let selectedUserType = 'usuário';
    
    // Elementos desktop
    const userTypeBtn = document.getElementById('userTypeBtn');
    const userTypeDropdown = document.getElementById('userTypeDropdown');
    const selectedType = document.getElementById('selectedType');
    const createBtn = document.getElementById('createBtn');
    const loginBtn = document.getElementById('loginBtn');
    
    // Elementos mobile
    const userTypeBtnMobile = document.getElementById('userTypeBtnMobile');
    const userTypeDropdownMobile = document.getElementById('userTypeDropdownMobile');
    const selectedTypeMobile = document.getElementById('selectedTypeMobile');
    const createBtnMobile = document.getElementById('createBtnMobile');
    const loginBtnMobile = document.getElementById('loginBtnMobile');
    
    // Elementos do menu mobile
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar');
    const sidebarClose = document.getElementById('sidebar-close');
    
    // Função para atualizar texto dos botões
    function updateButtonTexts() {
        const createText = selectedUserType === 'chef' ? 'Criar Conta como Chef' : 'Criar Conta como Usuário';
        const loginText = selectedUserType === 'chef' ? 'Entrar como Chef' : 'Entrar como Usuário';
        
        if (createBtn) createBtn.textContent = createText;
        if (loginBtn) loginBtn.textContent = loginText;
        if (createBtnMobile) createBtnMobile.textContent = createText;
        if (loginBtnMobile) loginBtnMobile.textContent = loginText;
    }
    
    // Função para redirecionar baseado no tipo de usuário
    function redirectToSignup() {
        if (selectedUserType === 'chef') {
            window.location.href = '/Cadastro-chef';
        } else {
            window.location.href = '/Criar-conta';
        }
    }
    
    // Função para toggle dropdown
    function toggleDropdown(btn, dropdown) {
        if (dropdown && btn) {
            dropdown.classList.toggle('show');
            btn.classList.toggle('active');
        }
    }
    
    // Função para selecionar tipo
    function selectUserType(type, typeDisplay, dropdown, btn) {
        selectedUserType = type;
        const displayText = type.charAt(0).toUpperCase() + type.slice(1);
        
        if (typeDisplay) typeDisplay.textContent = displayText;
        if (selectedType) selectedType.textContent = displayText;
        if (selectedTypeMobile) selectedTypeMobile.textContent = displayText;
        
        // Atualizar opções selecionadas
        document.querySelectorAll('.user-type-option').forEach(opt => {
            opt.classList.remove('selected');
            if (opt.dataset.type === type) {
                opt.classList.add('selected');
            }
        });
        
        if (dropdown) dropdown.classList.remove('show');
        if (btn) btn.classList.remove('active');
        updateButtonTexts();
    }
    
    // Event listeners para botões de criar conta
    if (createBtn) {
        createBtn.addEventListener('click', (e) => {
            e.preventDefault();
            redirectToSignup();
        });
    }
    
    if (createBtnMobile) {
        createBtnMobile.addEventListener('click', (e) => {
            e.preventDefault();
            redirectToSignup();
        });
    }
    
    // Event listeners para botões de login
    if (loginBtn) {
        loginBtn.addEventListener('click', (e) => {
            e.preventDefault();
            redirectToLogin();
        });
    }
    
    if (loginBtnMobile) {
        loginBtnMobile.addEventListener('click', (e) => {
            e.preventDefault();
            redirectToLogin();
        });
    }
    
    // Event listeners desktop para dropdown
    if (userTypeBtn && userTypeDropdown) {
        userTypeBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            toggleDropdown(userTypeBtn, userTypeDropdown);
        });
        
        userTypeDropdown.addEventListener('click', (e) => {
            if (e.target.classList.contains('user-type-option')) {
                selectUserType(e.target.dataset.type, selectedType, userTypeDropdown, userTypeBtn);
            }
        });
    }
    
    // Event listeners mobile para dropdown
    if (userTypeBtnMobile && userTypeDropdownMobile) {
        userTypeBtnMobile.addEventListener('click', (e) => {
            e.stopPropagation();
            toggleDropdown(userTypeBtnMobile, userTypeDropdownMobile);
        });
        
        userTypeDropdownMobile.addEventListener('click', (e) => {
            if (e.target.classList.contains('user-type-option')) {
                selectUserType(e.target.dataset.type, selectedTypeMobile, userTypeDropdownMobile, userTypeBtnMobile);
            }
        });
    }
    
    // Event listeners para menu mobile
    if (menuToggle) {
        menuToggle.addEventListener('click', () => {
            sidebar?.classList.add('active');
        });
    }
    
    if (sidebarClose) {
        sidebarClose.addEventListener('click', () => {
            sidebar?.classList.remove('active');
        });
    }
    
    // Fechar sidebar ao clicar fora
    document.addEventListener('click', (e) => {
        if (sidebar && sidebar.classList.contains('active') && 
            !sidebar.contains(e.target) && 
            !menuToggle.contains(e.target)) {
            sidebar.classList.remove('active');
        }
    });
    
    // Fechar dropdown ao clicar fora
    document.addEventListener('click', () => {
        if (userTypeDropdown) {
            userTypeDropdown.classList.remove('show');
            userTypeBtn?.classList.remove('active');
        }
        if (userTypeDropdownMobile) {
            userTypeDropdownMobile.classList.remove('show');
            userTypeBtnMobile?.classList.remove('active');
        }
    });
    
    // Inicializar texto dos botões
    updateButtonTexts();
});