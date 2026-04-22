// Additional sorting game enhancements
// Hover feedback
document.querySelectorAll('.draggable').forEach(item => {
    item.addEventListener('dragstart', () => {
        item.style.opacity = '0.5';
    });
    item.addEventListener('dragend', () => {
        item.style.opacity = '1';
    });
});

document.querySelectorAll('.basket').forEach(basket => {
    basket.addEventListener('dragover', (e) => {
        e.target.classList.add('drag-over');
    });
    basket.addEventListener('dragleave', (e) => {
        e.target.classList.remove('drag-over');
    });
});
