document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const termsList = document.getElementById('termsList');
    const termCards = document.querySelectorAll('.term-card');
    const noResults = document.getElementById('noResults');
    const alphabetLinks = document.querySelectorAll('.alphabet-link');
    const translations = document.getElementById('glossaryTranslations');
    // Search functionality
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        let visibleCount = 0;
        termCards.forEach(card => {
            const term = card.getAttribute('data-term');
            const synonyms = card.querySelector('.tag') ? Array.from(card.querySelectorAll('.tag')).map(tag => tag.textContent.toLowerCase()) : [];
            const matches = term.includes(searchTerm) ||  synonyms.some(synonym => synonym.includes(searchTerm));
            if (matches || searchTerm === '') {
                card.style.display = 'block';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });
        // Show/hide no results message
        if (visibleCount === 0 && searchTerm !== '') {
            noResults.classList.remove('is-hidden');
            termsList.classList.add('is-hidden');
        } else {
            noResults.classList.add('is-hidden');
            termsList.classList.remove('is-hidden');
        }
    });
    // Alphabet navigation
    alphabetLinks.forEach(link => {
        link.addEventListener('click', function() {
            const letter = this.getAttribute('data-letter');
            termCards.forEach(card => {
                const firstLetter = card.getAttribute('data-first-letter');
                if (firstLetter === letter) {
                    card.style.display = 'block';
                    card.scrollIntoView({ behavior: 'smooth', block: 'start' });
                } else {
                    card.style.display = 'none';
                }
            });
            searchInput.value = '';
            noResults.classList.add('is-hidden');
            termsList.classList.remove('is-hidden');
        });
    });
    // Handle term link copy buttons
    document.querySelectorAll('.copy-term-link').forEach(btn => {
        btn.addEventListener('click', async function() {
            const url = `${location.origin}${location.pathname}#${this.dataset.key}`;
            const success = await copyToClipboard(url);
            showFeedback(this, success, translations);
        });
    });
    async function copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text);
            return true;
        } catch (err) {
            return false;
        }
    }
    function showFeedback(btn, success, translations) {
        const icon = btn.querySelector('i');
        const originalIcon = icon.className;
        // Set feedback state
        icon.className = success ? 'fas fa-check' : 'fas fa-times';
        // Restore original state after 2 seconds
        setTimeout(() => {
            icon.className = originalIcon;
        }, 2000);
    }
});