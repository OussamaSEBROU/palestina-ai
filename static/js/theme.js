// theme.js - Gestion du thème clair/sombre pour Palestina-ai

document.addEventListener('DOMContentLoaded', function() {
    // Récupérer le bouton de changement de thème
    const themeToggle = document.getElementById('theme-toggle');
    
    // Vérifier si un thème est déjà enregistré dans le localStorage
    const currentTheme = localStorage.getItem('theme') || 'light';
    
    // Appliquer le thème actuel
    document.body.className = 'theme-' + currentTheme;
    
    // Mettre à jour l'icône du bouton
    updateThemeIcon(currentTheme);
    
    // Ajouter un écouteur d'événement pour le changement de thème
    themeToggle.addEventListener('click', function() {
        // Basculer entre les thèmes
        const newTheme = document.body.classList.contains('theme-light') ? 'dark' : 'light';
        
        // Appliquer le nouveau thème
        document.body.className = 'theme-' + newTheme;
        
        // Enregistrer le thème dans le localStorage
        localStorage.setItem('theme', newTheme);
        
        // Mettre à jour l'icône du bouton
        updateThemeIcon(newTheme);
    });
    
    // Fonction pour mettre à jour l'icône du bouton
    function updateThemeIcon(theme) {
        const icon = themeToggle.querySelector('i');
        if (theme === 'dark') {
            icon.className = 'fas fa-sun';
        } else {
            icon.className = 'fas fa-moon';
        }
    }
});
