
const toggle = document.querySelector('.toggle');
const nav = document.querySelector('header nav');

// Open and close the mobile navigation menu.
if (toggle && nav) {
    toggle.addEventListener('click', () => {
        const isOpen = nav.classList.toggle('open');

        toggle.setAttribute('aria-expanded', String(isOpen));
        toggle.textContent = isOpen ? '×' : '☰';
    });

    // Close the menu after clicking a navigation link on mobile.
    nav.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            if (window.innerWidth <= 760) {
                nav.classList.remove('open');
                toggle.setAttribute('aria-expanded', 'false');
                toggle.textContent = '☰';
            }
        });
    });
}

// Highlight the current page in the navigation menu.
const currentPath =
    window.location.pathname.replace(/\/$/, '') || '/';

document.querySelectorAll('header nav > a').forEach(link => {
    const path = new URL(link.href, window.location.origin)
        .pathname.replace(/\/$/, '') || '/';

    if (path === currentPath) {
        link.classList.add('active');
        link.setAttribute('aria-current', 'page');
    }
});

// Filter products by their selected category.
const filterButtons = document.querySelectorAll('.filter-btn');
const productCards = document.querySelectorAll('.product-card');
const noResults = document.querySelector('.no-results');

filterButtons.forEach(button => {
    button.addEventListener('click', () => {
        const selected = button.dataset.filter;

        // Update the active filter button.
        filterButtons.forEach(btn => {
            const isActive = btn === button;

            btn.classList.toggle('active', isActive);
            btn.setAttribute('aria-pressed', String(isActive));
        });

        // Show products that match the selected category.
        let visible = 0;

        productCards.forEach(card => {
            const shouldShow =
                selected === 'all' ||
                card.dataset.category === selected;

            card.hidden = !shouldShow;

            if (shouldShow) {
                visible++;
            }
        });

        // Display a message if no products match the filter.
        if (noResults) {
            noResults.hidden = visible > 0;
        }

        // Scroll to the selected category.
        if (selected !== 'all') {
            const target = document.getElementById(selected);

            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
});
