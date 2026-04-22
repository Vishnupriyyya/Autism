// Object identification game logic
let currentTask = ['red_ball', 'blue_cloud', 'green_tree'][Math.floor(Math.random() * 3)];
let lineDrawing = null;

const audioClips = {
    'red_ball': new Audio('/static/audio/red_ball.mp3'),
    'blue_cloud': new Audio('/static/audio/blue_cloud.mp3'),
    'green_tree': new Audio('/static/audio/green_tree.mp3')
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    playInstructionAudio();
});

function playAudio(objectId) {
    const audio = audioClips[objectId];
    if (audio) {
        audio.currentTime = 0;
        audio.volume = 0.8;
        audio.play().catch(e => {
            // Fallback visual feedback
            const icon = event.target;
            icon.style.background = '#4caf50';
            setTimeout(() => icon.style.background = '#ff9800', 300);
        });
    }
}

function playInstructionAudio() {
    playAudio(currentTask);
}

function selectObject(objectId) {
    // Visual feedback
    document.querySelectorAll('.item').forEach(item => item.classList.remove('selected'));
    event.currentTarget.classList.add('selected');
    
    // Optional: highlight matching task button
    document.querySelectorAll('.task-btn').forEach(btn => btn.style.opacity = '0.6');
    const matchingBtn = Array.from(document.querySelectorAll('.task-btn')).find(btn => btn.onclick.toString().includes(objectId));
    if (matchingBtn) matchingBtn.style.opacity = '1';
}

function checkMatch(selectedObjectId) {
    const feedback = document.getElementById('feedback');
    
    if (selectedObjectId === currentTask) {
        feedback.innerHTML = "Excellent identification! 🎉✨";
        feedback.className = 'feedback-bubble feedback-success';
        
        // Connect with animated line
        const objectEl = document.getElementById(selectedObjectId);
        const canvas = document.getElementById('lineCanvas');
        drawAnimatedLine(objectEl, event.target);
        
        // Stars animation
        showStarReward();
        setTimeout(() => location.reload(), 4000);
    } else {
        feedback.innerHTML = "Try listening to the instruction again! 🔊";
        feedback.className = 'feedback-bubble feedback-error';
        setTimeout(() => {
            feedback.innerHTML = '';
            feedback.className = 'feedback-bubble';
        }, 3000);
    }
}

function drawAnimatedLine(fromEl, toEl) {
    const canvas = document.getElementById('lineCanvas');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
    const fromRect = fromEl.getBoundingClientRect();
    const toRect = toEl.getBoundingClientRect();
    
    const startX = fromRect.left + fromRect.width / 2 + window.scrollX;
    const startY = fromRect.top + fromRect.height / 2 + window.scrollY;
    const endX = toRect.left + toRect.width / 2 + window.scrollX;
    const endY = toRect.top + toRect.height / 2 + window.scrollY;
    
    // Animated dashed line
    let progress = 0;
    const animateLine = () => {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.lineWidth = 8;
        ctx.lineCap = 'round';
        ctx.strokeStyle = '#4caf50';
        ctx.setLineDash([15, 15]);
        ctx.shadowColor = '#4caf50';
        ctx.shadowBlur = 15;
        
        ctx.beginPath();
        ctx.moveTo(startX, startY);
        ctx.lineTo(startX + (endX - startX) * progress, startY + (endY - startY) * progress);
        ctx.stroke();
        
        progress += 0.08;
        if (progress < 1) {
            requestAnimationFrame(animateLine);
        } else {
            // Celebrate with sparkle
            ctx.strokeStyle = '#ffeb3b';
            ctx.lineDashOffset = -30;
            ctx.stroke();
        }
    };
    animateLine();
}

function showStarReward() {
    const stars = ['⭐', '✨', '🎉', '🌟'];
    for (let i = 0; i < 25; i++) {
        setTimeout(() => {
            const star = document.createElement('div');
            star.textContent = stars[Math.floor(Math.random() * stars.length)];
            star.style.cssText = `
                position: fixed;
                left: 50vw;
                top: 50vh;
                font-size: ${30 + Math.random() * 30}px;
                pointer-events: none;
                z-index: 9999;
                animation: starExplode 1.5s forwards;
            `;
            document.body.appendChild(star);
            setTimeout(() => star.remove(), 1500);
        }, i * 80);
    }
}

