document.addEventListener('DOMContentLoaded', () => {
    // Mobile menu toggle
    const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

    $navbarBurgers.forEach(el => {
        el.addEventListener('click', () => {
            const target = el.dataset.target;
            const $target = document.getElementById(target);
            el.classList.toggle('is-active');
            $target.classList.toggle('is-active');
        });
    });

    // Copy button for code blocks
    document.querySelectorAll('.article-body pre > code').forEach(code => {
        const pre = code.parentElement;
        if (pre.hasAttribute('data-no-copy')) return;

        const wrap = document.createElement('div');
        wrap.className = 'code-block';
        pre.parentNode.insertBefore(wrap, pre);
        wrap.appendChild(pre);

        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'button is-small is-info is-light copy-code-btn';
        btn.innerHTML = '<i class="fas fa-copy"></i>';
        wrap.appendChild(btn);

        btn.addEventListener('click', async () => {
            try {
                await navigator.clipboard.writeText(code.innerText);
                const icon = btn.querySelector('i');
                icon.className = 'fas fa-check';
                setTimeout(() => icon.className = 'fas fa-copy', 2000);
            } catch (e) {
                console.error('Copy failed:', e);
            }
        });
    });
});