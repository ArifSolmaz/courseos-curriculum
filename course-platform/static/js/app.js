// CourseOS Platform — Client-side JavaScript

// Collapsible sections
document.querySelectorAll('.collapsible-header').forEach(header => {
    header.addEventListener('click', () => {
        const body = header.nextElementSibling;
        body.classList.toggle('open');
        const arrow = header.querySelector('.arrow');
        if (arrow) {
            arrow.textContent = body.classList.contains('open') ? '▾' : '▸';
        }
    });
});

// Auto-dismiss flash messages after 5 seconds
document.querySelectorAll('.flash').forEach(flash => {
    setTimeout(() => {
        flash.style.opacity = '0';
        flash.style.transition = 'opacity 0.5s';
        setTimeout(() => flash.remove(), 500);
    }, 5000);
});

// Confirm destructive actions
document.querySelectorAll('[data-confirm]').forEach(el => {
    el.addEventListener('click', (e) => {
        if (!confirm(el.dataset.confirm)) {
            e.preventDefault();
        }
    });
});

// Progress animation on page load
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.progress-fill').forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0%';
        requestAnimationFrame(() => {
            requestAnimationFrame(() => {
                bar.style.width = width;
            });
        });
    });
});

// API helpers for future AJAX features
const api = {
    async get(url) {
        const response = await fetch(url);
        return response.json();
    },

    async getProgress() {
        return this.get('/api/progress');
    },

    async getTimeline() {
        return this.get('/api/timeline');
    }
};
