// Wait for the page to be fully loaded
document.addEventListener('DOMContentLoaded', () => {

    // Find all product cards on the page
    const cards = document.querySelectorAll('.product-card-link');

    // Loop through each card
    cards.forEach((card, index) => {
        // Apply a staggered delay to each card
        setTimeout(() => {
            card.classList.add('is-visible');
        }, 100 * index); // 100ms delay per card
    });

});