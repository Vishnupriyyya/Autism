function checkAnswer(emotion) {
    const feedback = document.getElementById('feedback');
    const buttons = document.querySelectorAll('.btn-emotion');
    const targetEmotion = document.getElementById('targetEmotion').textContent.toLowerCase();
    
    buttons.forEach(btn => btn.disabled = true);
    
    setTimeout(() => {
        if (emotion === targetEmotion) {
            feedback.innerHTML = `Perfect! That's the <strong>${targetEmotion.toUpperCase()}</strong> face! 🎉⭐⭐⭐`;
            feedback.className = 'feedback success';
            confettiEffect();
            document.querySelectorAll('.face[data-emotion="${targetEmotion}"]').forEach(face => {
                face.style.borderColor = '#00b894';
                face.style.transform = 'scale(1.1)';
            });
            setTimeout(() => location.reload(), 4000);
        } else {
            feedback.innerHTML = `No! That's ${emotion.toUpperCase()}. The ${targetEmotion.toUpperCase()} face is smiling! 😊`;
            feedback.className = 'feedback error';
            document.querySelector(`.btn-emotion[onclick="checkAnswer('${emotion}')"]`).classList.add('wrong');
            setTimeout(() => {
                feedback.innerHTML = '';
                feedback.className = 'feedback';
                buttons.forEach(btn => btn.disabled = false);
                document.querySelector('.btn-emotion.wrong')?.classList.remove('wrong');
            }, 3500);
        }
    }, 200);
}

// Reuse confetti from previous games
function confettiEffect() {
    const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#f9ca24', '#f0932b', '#eb4d4b'];
    for (let i = 0; i < 60; i++) {
        setTimeout(() => {
            const confetti = document.createElement('div');
            confetti.style.cssText = `
                position: fixed;
                left: ${Math.random() * 100}vw;
                top: -10vh;
                width: 10px; height: 10px;
                background: ${colors[Math.floor(Math.random() * colors.length)]};
                border-radius: 50%;
                pointer-events: none;
                z-index: 1000;
                animation: confettiFall 3s linear forwards;
            `;
            document.body.appendChild(confetti);
            setTimeout(() => confetti.remove(), 3000);
        }, i * 30);
    }
}

