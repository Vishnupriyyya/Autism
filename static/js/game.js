// Universal Game Engine - Shared across all activities
// Core event handlers and animations

// Confetti and particle systems
function confettiEffect(type = 'stars') {
    const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#f9ca24', '#f0932b', '#eb4d4b', '#6c5ce7', '#a29bfe', '#fdcb6e', '#e17055'];
    const emojis = ['⭐', '✨', '🎉', '🎊', '🌟', '💫'];
    
    for (let i = 0; i < 100; i++) {
        setTimeout(() => {
            const particle = document.createElement('div');
            particle.innerHTML = emojis[Math.floor(Math.random() * emojis.length)];
            particle.style.cssText = `
                position: fixed;
                left: ${Math.random() * 100}vw;
                top: -15vh;
                font-size: ${25 + Math.random() * 25}px;
                pointer-events: none;
                z-index: 10000;
                color: ${colors[Math.floor(Math.random() * colors.length)]};
                animation: particleFall ${2.5 + Math.random()}s linear forwards;
                transform: rotate(${Math.random() * 360}deg);
            `;
            document.body.appendChild(particle);
            setTimeout(() => particle.remove(), 4000);
        }, i * 20);
    }
}

// Star rating system
function updateStars(correct = true) {
    const stars = document.querySelector('.stars');
    if (correct) {
        stars.innerHTML = '⭐⭐⭐';
        stars.style.animation = 'sparkle 0.5s';
    } else {
        stars.innerHTML = '☆☆☆';
    }
    setTimeout(() => stars.innerHTML = '☆☆☆', 1500);
}

// Universal answer checker
function checkAnswer(selected, correct, feedbackId = 'feedback') {
    const feedback = document.getElementById(feedbackId);
    
    if (selected === correct) {
        feedback.innerHTML = "Great Job! 🎉";
        feedback.className = 'feedback-bubble feedback-success';
        confettiEffect();
        updateStars(true);
        
        // Disable further interaction
        document.querySelectorAll('[onclick]').forEach(el => el.style.pointerEvents = 'none');
        
        setTimeout(() => {
            // Next level or restart
            location.reload();
        }, 3000);
    } else {
        feedback.innerHTML = "Try again! 🔄";
        feedback.className = 'feedback-bubble feedback-error';
        updateStars(false);
        setTimeout(() => {
            feedback.innerHTML = '';
            feedback.className = 'feedback-bubble';
        }, 2000);
    }
}

// Drag and drop utilities
function allowDrop(ev) {
    ev.preventDefault();
    ev.target.classList.add('drag-over');
}

function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
    ev.target.style.opacity = '0.7';
}

function drop(ev) {
    ev.preventDefault();
    const data = ev.dataTransfer.getData("text");
    ev.target.appendChild(document.getElementById(data));
    ev.target.classList.remove('drag-over');
    
    // Check if correct drop
    if (ev.target.dataset.correct === data) {
        checkAnswer(data, data, 'feedback');
    } else {
        document.getElementById('feedback').innerHTML = "Not the right place!";
    }
}

// LeaderLine integration (for matching games with lines)
function connectElements(startId, endId, color = '#2fbdbb') {
    if (typeof LeaderLine !== 'undefined') {
        const line = new LeaderLine(
            document.getElementById(startId),
            document.getElementById(endId),
            { 
                color: color,
                size: 4,
                path: 'straight',
                startSocket: 'auto',
                endSocket: 'auto'
            }
        );
        setTimeout(() => line.remove(), 3000);
    }
}

// Audio utilities
function playSound(soundType = 'success') {
    const sounds = {
        success: new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJIgYJghYhbiWSICDY...'),
        error: new Audio('data:audio/wav;base64,UklGRiQDAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJI...'),
        click: new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJI...')
    };
    
    if (sounds[soundType]) {
        sounds[soundType].play().catch(() => {}); 
    }
}

// Progress tracking (localStorage fallback)
function saveProgress(gameName, score) {
    const progress = JSON.parse(localStorage.getItem('autismGames') || '{}');
    progress[gameName] = score;
    localStorage.setItem('autismGames', JSON.stringify(progress));
}

// Touch-friendly enhancements
document.addEventListener('touchstart', function() {}, { passive: true });

// Game pause/resume
let gamePaused = false;
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        gamePaused = true;
    } else {
        gamePaused = false;
    }
});

// Initialize all games on load
document.addEventListener('DOMContentLoaded', function() {
    // Preload common assets
    playSound('click');
    
    // Add touch ripple effect to buttons
    document.querySelectorAll('button, .shape, .item').forEach(el => {
        el.addEventListener('click', function(e) {
            playSound('click');
        });
    });
});

