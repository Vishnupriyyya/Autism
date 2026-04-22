// Matching game state
let selectedImage = null;

function selectImage(imgId) {
    // Reset previous selections
    document.querySelectorAll('.match-img').forEach(img => {
        img.parentElement.classList.remove('selected');
    });
    
    // Select new image
    const itemBox = document.getElementById(imgId + '-img').parentElement;
    itemBox.classList.add('selected');
    selectedImage = imgId;
    
    // Visual feedback
    const feedback = document.getElementById('feedback');
    feedback.innerHTML = 'Now choose the word!';
    feedback.className = 'feedback-bubble';
}

function checkMatch(word) {
    const feedback = document.getElementById('feedback');
    
    if (!selectedImage) {
        feedback.innerHTML = 'Please first select a picture! 📸';
        feedback.className = 'feedback-bubble feedback-error';
        setTimeout(() => feedback.innerHTML = '', 2000);
        return;
    }
    
    if (selectedImage === word) {
        feedback.innerHTML = `Perfect! "${word.toUpperCase()}" matches the picture! 🎉⭐⭐⭐`;
        feedback.className = 'feedback-bubble feedback-success';
        document.querySelectorAll('.word-btn, .match-img').forEach(el => {
            el.style.pointerEvents = 'none';
            el.style.opacity = '0.7';
        });
        confettiEffect('rainbow');
        setTimeout(() => location.reload(), 4000);
    } else {
        feedback.innerHTML = `"${word.toUpperCase()}" doesn't match your picture. Try again! 🔄`;
        feedback.className = 'feedback-bubble feedback-error';
        setTimeout(() => {
            feedback.innerHTML = '';
            feedback.className = 'feedback-bubble';
        }, 2500);
    }
}

// Enhanced confetti with rainbow colors
function confettiEffect(type = 'stars') {
    const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#f9ca24', '#f0932b', '#eb4d4b', '#6c5ce7', '#a29bfe'];
    const emojis = type === 'rainbow' ? ['🌈', '⭐', '✨', '🎉', '🎊'] : ['⭐'];
    
    for (let i = 0; i < 80; i++) {
        setTimeout(() => {
            const particle = document.createElement('div');
            particle.textContent = emojis[Math.floor(Math.random() * emojis.length)];
            particle.style.cssText = `
                position: fixed;
                left: ${Math.random() * 100}vw;
                animation: confettiRain ${2 + Math.random() * 2}s linear forwards;
                font-size: ${20 + Math.random() * 20}px;
                pointer-events: none;
                z-index: 9999;
                color: ${colors[Math.floor(Math.random() * colors.length)]};
                top: -10vh;
            `;
            document.body.appendChild(particle);
            setTimeout(() => particle.remove(), 5000);
        }, i * 25);
    }
}

