const words = ["Developers", "Enterprises", "Data Centers", "Startups", "Security Teams"];
let index = 0;
const rotatingText = document.getElementById("rotating-text");

setInterval(() => {
    index = (index + 1) % words.length;
    rotatingText.style.animation = "none";
    void rotatingText.offsetWidth;
    rotatingText.textContent = words[index];
    rotatingText.style.animation = "fadeSlide 0.5s ease";
}, 2000);