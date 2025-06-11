
document.addEventListener('DOMContentLoaded', function() {
    // Verifica se a largura da tela é menor que 768px (dispositivos móveis)
    if (window.innerWidth < 768) {
        const video = document.getElementById('bg-video');
        const backgroundDiv = document.querySelector('.background-video');
        
        // Remove o vídeo
        if (video) {
            video.remove();
        }
        
        // Adiciona uma imagem de fundo em vez do vídeo
        if (backgroundDiv) {
            backgroundDiv.style.backgroundImage = 'url("../static/Video/Video_mobile.mp4")';
            backgroundDiv.style.backgroundSize = 'cover';
            backgroundDiv.style.backgroundPosition = 'center';
        }
    }
});