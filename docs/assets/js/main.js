// Mobile Navigation
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

if (hamburger) {
    hamburger.addEventListener('click', () => {
        navMenu.classList.toggle('active');
        hamburger.classList.toggle('active');
    });
}

// Active Navigation Link
const navLinks = document.querySelectorAll('.nav-link');
const sections = document.querySelectorAll('section[id]');

function highlightNavigation() {
    const scrollY = window.pageYOffset;

    sections.forEach(section => {
        const sectionHeight = section.offsetHeight;
        const sectionTop = section.offsetTop - 100;
        const sectionId = section.getAttribute('id');

        if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${sectionId}`) {
                    link.classList.add('active');
                }
            });
        }
    });
}

window.addEventListener('scroll', highlightNavigation);

// Enhanced Smooth Scroll for Navigation Links
navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href && href.includes('#')) {
        link.addEventListener('click', (e) => {
            // Check if it's an internal link
            if (href.startsWith('#')) {
                e.preventDefault();
                const targetId = href;
                const targetSection = document.querySelector(targetId);
                
                if (targetSection) {
                    const targetPosition = targetSection.offsetTop - 80;
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                    
                    // Update URL without reload
                    history.pushState(null, null, targetId);
                    
                    // Close mobile menu
                    navMenu.classList.remove('active');
                    if (hamburger) hamburger.classList.remove('active');
                }
            } else if (href.includes('.html#')) {
                // For cross-page anchors
                const [page, anchor] = href.split('#');
                if (window.location.pathname.includes(page)) {
                    e.preventDefault();
                    const targetSection = document.querySelector('#' + anchor);
                    if (targetSection) {
                        targetSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }
                }
            }
        });
    }
});

// Enhanced Scroll to Top Button
const scrollTopBtn = document.createElement('div');
scrollTopBtn.className = 'scroll-top';
scrollTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
scrollTopBtn.title = 'Нагору';
scrollTopBtn.setAttribute('aria-label', 'Прокрутити нагору');
document.body.appendChild(scrollTopBtn);

window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
        scrollTopBtn.classList.add('show');
    } else {
        scrollTopBtn.classList.remove('show');
    }
});

scrollTopBtn.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

// Animate on Scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'fadeInUp 0.6s ease forwards';
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Add animation to elements (without initial opacity)
document.querySelectorAll('.feature-card, .scenario-card, .stat-card').forEach(el => {
    // Removed initial opacity setting for better UX
    observer.observe(el);
});

// CSS Animation
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeInUp {
        from {
            opacity: 0.7;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .hamburger.active span:nth-child(1) {
        transform: rotate(45deg) translate(5px, 5px);
    }
    
    .hamburger.active span:nth-child(2) {
        opacity: 0;
    }
    
    .hamburger.active span:nth-child(3) {
        transform: rotate(-45deg) translate(7px, -6px);
    }
`;
document.head.appendChild(style);

// Counter Animation for Stats
function animateCounter(element, target, duration = 2000) {
    const start = 0;
    const increment = target / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = target + (element.textContent.includes('%') ? '%' : '');
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current) + (element.textContent.includes('%') ? '%' : '');
        }
    }, 16);
}

// Animate stats when they come into view
const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const statNumbers = entry.target.querySelectorAll('.stat-number');
            statNumbers.forEach(stat => {
                const text = stat.textContent;
                const number = parseInt(text.replace(/\D/g, ''));
                if (!isNaN(number)) {
                    animateCounter(stat, number);
                }
            });
            statsObserver.unobserve(entry.target);
        }
    });
}, observerOptions);

const heroStats = document.querySelector('.hero-stats');
if (heroStats) {
    statsObserver.observe(heroStats);
}

// Progress Bar Animation
const progressObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const progressFill = entry.target.querySelector('.progress-fill');
            if (progressFill) {
                progressFill.style.animation = 'progressAnimation 2s ease forwards';
            }
            progressObserver.unobserve(entry.target);
        }
    });
}, observerOptions);

document.querySelectorAll('.error-reduction').forEach(el => {
    progressObserver.observe(el);
});

// Add loading state for buttons
document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('click', function(e) {
        if (this.getAttribute('href') && !this.getAttribute('href').startsWith('#')) {
            this.classList.add('loading');
            this.innerHTML = '<span class="loading"></span> Завантаження...';
        }
    });
});

// Copy code blocks (if any)
document.addEventListener('DOMContentLoaded', () => {
    const codeBlocks = document.querySelectorAll('pre code');
    
    codeBlocks.forEach(block => {
        const wrapper = document.createElement('div');
        wrapper.className = 'code-wrapper';
        block.parentNode.insertBefore(wrapper, block);
        wrapper.appendChild(block);
        
        const copyBtn = document.createElement('button');
        copyBtn.className = 'copy-btn';
        copyBtn.innerHTML = '<i class="fas fa-copy"></i> Copy';
        wrapper.appendChild(copyBtn);
        
        copyBtn.addEventListener('click', () => {
            navigator.clipboard.writeText(block.textContent).then(() => {
                copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
                setTimeout(() => {
                    copyBtn.innerHTML = '<i class="fas fa-copy"></i> Copy';
                }, 2000);
            });
        });
    });
});

// Theme Toggle (optional)
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

// Initialize theme on load
initTheme();

// Search functionality (for documentation pages)
function initSearch() {
    const searchInput = document.getElementById('search');
    if (!searchInput) return;
    
    searchInput.addEventListener('input', (e) => {
        const searchTerm = e.target.value.toLowerCase();
        const searchableElements = document.querySelectorAll('[data-searchable]');
        
        searchableElements.forEach(element => {
            const text = element.textContent.toLowerCase();
            if (text.includes(searchTerm)) {
                element.style.display = '';
                element.classList.add('highlight');
            } else {
                element.style.display = 'none';
                element.classList.remove('highlight');
            }
        });
    });
}

// Initialize search on documentation pages
initSearch();

// Lazy Loading for Images
const imageObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const img = entry.target;
            if (img.dataset.src) {
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        }
    });
});

document.querySelectorAll('img[data-src]').forEach(img => {
    imageObserver.observe(img);
});

// Console Easter Egg
console.log('%c🚀 HR Integration System', 'color: #4F46E5; font-size: 24px; font-weight: bold;');
console.log('%cРозроблено з ❤️ для Vira Games', 'color: #7C3AED; font-size: 14px;');
console.log('%cАвтор: Дубовик Кирило', 'color: #6B7280; font-size: 12px;');

// Simple search functionality for navigation
const searchInput = document.getElementById('nav-search');
if (searchInput) {
    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase();
        if (query.length > 2) {
            // Simple search - redirect to docs page with search query
            if (e.key === 'Enter') {
                window.location.href = `docs.html?search=${encodeURIComponent(query)}`;
            }
        }
    });
    
    // Handle Enter key
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && e.target.value.length > 0) {
            window.location.href = `docs.html?search=${encodeURIComponent(e.target.value)}`;
        }
    });
}