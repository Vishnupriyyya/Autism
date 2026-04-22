function checkAnswer(shapeType) {
    const dropZone = document.querySelector('.drop-zone');
    const feedback = document.getElementById('feedback');
    const options = document.querySelectorAll('.option');
    
    options.forEach(opt => opt.style.pointerEvents = 'none');
    
    if (shapeType === 'heart') {
        dropZone.innerHTML = '<div class="shape heart"></div>';
        dropZone.style.background = 'rgba(0, 184, 148, 0.2)';
        dropZone.style.borderColor = '#00b894';
        
        feedback.innerHTML = "Perfect! You completed the pattern! 🎉⭐";
        feedback.style.color = "green";
        feedback.style.fontSize = "1.3rem";
        
        document.querySelector('.option[onclick="checkAnswer(\'heart\')"]').classList.add('correct');
        confettiEffect();
        
        setTimeout(() => location.reload(), 3000);
    } else {
        feedback.innerHTML = "Not quite. Look for the repeating pattern! 🔍";
        feedback.style.color = "orange";
        setTimeout(() => {
            feedback.innerHTML = '';
            options.forEach(opt => opt.style.pointerEvents = 'auto');
        }, 2500);
    }
}

// Confetti stars animation
function confettiEffect() {
    for (let i = 0; i < 30; i++) {
        setTimeout(() => {
            const star = document.createElement('div');
            star.textContent = '⭐';
            star.style.cssText = `
                position: fixed;
                left: ${Math.random() * 100}vw;
                top: -10vh;
                font-size: ${12 + Math.random() * 16}px;
                pointer-events: none;
                z-index: 1000;
                animation: starFall 2.5s linear forwards;
            `;
            document.body.appendChild(star);
            setTimeout(() => star.remove(), 2500);
        }, i * 60);
    }
}

