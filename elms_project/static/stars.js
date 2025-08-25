document.addEventListener('DOMContentLoaded', function() {
    const starsContainer = document.getElementById('stars');
    const starsCount = 200;
    
    // Create stars
    for (let i = 0; i < starsCount; i++) {
        createStar();
    }
    
    function createStar() {
        const star = document.createElement('div');
        star.classList.add('star');
        
        // Random size between 1-4px
        const size = Math.random() * 3 + 1;
        star.style.width = `${size}px`;
        star.style.height = `${size}px`;
        
        // Random position
        const x = Math.random() * 100;
        const y = Math.random() * 100;
        star.style.left = `${x}vw`;
        star.style.top = `${y}vh`;
        
        // Random animation duration between 3-8 seconds
        const duration = Math.random() * 5 + 3;
        star.style.animationDuration = `${duration}s`;
        
        // Random animation delay
        const delay = Math.random() * 5;
        star.style.animationDelay = `${delay}s`;
        
        starsContainer.appendChild(star);
    }
});