// Typewriter effect for rotating text
const phrases = [
    "No te compliques",
    "No te pierdas",
    "No te enojes",
    "No te estreses"
];

let phraseIndex = 0;
let charIndex = 0;
let isDeleting = false;
let typingSpeed = 100;
let rotatingText;

function typeWriter() {
    if (!rotatingText) return;

    const currentPhrase = phrases[phraseIndex];

    // Limpiar el contenido actual
    rotatingText.textContent = '';

    if (isDeleting) {
        // Borrando texto
        const newText = currentPhrase.substring(0, charIndex - 1);
        rotatingText.textContent = newText || '\u00A0';
        charIndex--;
        typingSpeed = 50;
    } else {
        // Escribiendo texto
        rotatingText.textContent = currentPhrase.substring(0, charIndex + 1);
        charIndex++;
        typingSpeed = 100;
    }

    // Agregar cursor al final
    const cursor = document.createElement('span');
    cursor.className = 'cursor';
    cursor.textContent = '|';
    rotatingText.appendChild(cursor);

    // Si termino de escribir la frase
    if (!isDeleting && charIndex === currentPhrase.length) {
        // Pausa antes de empezar a borrar
        typingSpeed = 2000;
        isDeleting = true;
    }

    // Si termino de borrar la frase
    if (isDeleting && charIndex === 0) {
        isDeleting = false;
        phraseIndex = (phraseIndex + 1) % phrases.length;
        typingSpeed = 500;
    }

    setTimeout(typeWriter, typingSpeed);
}

// Iniciar el efecto cuando cargue la pagina
document.addEventListener('DOMContentLoaded', () => {
    rotatingText = document.getElementById('rotating-text');
    if (rotatingText) {
        setTimeout(typeWriter, 1000);
    }
});
