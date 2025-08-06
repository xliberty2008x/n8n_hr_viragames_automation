// Documentation Specific JavaScript

// Sidebar Navigation
document.addEventListener('DOMContentLoaded', () => {
    // Active sidebar link based on scroll position
    const sidebarLinks = document.querySelectorAll('.sidebar-link');
    const sections = document.querySelectorAll('.docs-section[id]');
    
    function updateActiveLink() {
        const scrollY = window.pageYOffset;
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop - 100;
            const sectionBottom = sectionTop + section.offsetHeight;
            const sectionId = section.getAttribute('id');
            
            if (scrollY >= sectionTop && scrollY < sectionBottom) {
                sidebarLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${sectionId}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }
    
    window.addEventListener('scroll', updateActiveLink);
    
    // Smooth scroll for sidebar links
    sidebarLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                const targetPosition = targetSection.offsetTop - 80;
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Collapsible sections
    const collapsibleHeaders = document.querySelectorAll('.collapsible-header');
    
    collapsibleHeaders.forEach(header => {
        header.addEventListener('click', () => {
            const content = header.nextElementSibling;
            const icon = header.querySelector('.collapse-icon');
            
            content.classList.toggle('collapsed');
            icon.classList.toggle('rotated');
        });
    });
    
    // Code block enhancements
    enhanceCodeBlocks();
    
    // Search functionality
    initDocSearch();
    
    // Table of contents generator
    generateTableOfContents();
});

// Enhance code blocks with line numbers and copy functionality
function enhanceCodeBlocks() {
    const codeBlocks = document.querySelectorAll('pre code');
    
    codeBlocks.forEach(block => {
        // Add line numbers
        const lines = block.textContent.split('\n');
        if (lines.length > 1) {
            const lineNumbers = document.createElement('div');
            lineNumbers.className = 'line-numbers';
            
            for (let i = 1; i <= lines.length; i++) {
                const lineNumber = document.createElement('span');
                lineNumber.textContent = i;
                lineNumbers.appendChild(lineNumber);
            }
            
            block.parentElement.insertBefore(lineNumbers, block);
            block.parentElement.classList.add('has-line-numbers');
        }
        
        // Add language label
        const language = block.className.match(/language-(\w+)/);
        if (language) {
            const label = document.createElement('span');
            label.className = 'code-language';
            label.textContent = language[1].toUpperCase();
            block.parentElement.appendChild(label);
        }
    });
}

// Documentation search
function initDocSearch() {
    const searchContainer = document.createElement('div');
    searchContainer.className = 'doc-search';
    searchContainer.innerHTML = `
        <div class="search-box">
            <i class="fas fa-search"></i>
            <input type="text" id="doc-search" placeholder="Пошук в документації...">
            <kbd>Ctrl+K</kbd>
        </div>
        <div class="search-results" id="search-results"></div>
    `;
    
    const sidebar = document.querySelector('.docs-sidebar');
    if (sidebar) {
        sidebar.insertBefore(searchContainer, sidebar.firstChild);
    }
    
    const searchInput = document.getElementById('doc-search');
    const searchResults = document.getElementById('search-results');
    
    if (searchInput) {
        // Keyboard shortcut
        document.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                searchInput.focus();
            }
        });
        
        // Search functionality
        searchInput.addEventListener('input', debounce((e) => {
            const query = e.target.value.toLowerCase();
            
            if (query.length < 2) {
                searchResults.innerHTML = '';
                searchResults.style.display = 'none';
                return;
            }
            
            const results = searchDocumentation(query);
            displaySearchResults(results, searchResults, query);
        }, 300));
        
        // Close search on outside click
        document.addEventListener('click', (e) => {
            if (!searchContainer.contains(e.target)) {
                searchResults.style.display = 'none';
            }
        });
    }
}

// Search through documentation content
function searchDocumentation(query) {
    const sections = document.querySelectorAll('.docs-section');
    const results = [];
    
    sections.forEach(section => {
        const title = section.querySelector('h1, h2, h3');
        const content = section.textContent.toLowerCase();
        
        if (content.includes(query)) {
            const snippet = extractSnippet(content, query);
            results.push({
                title: title ? title.textContent : 'Untitled Section',
                snippet: snippet,
                element: section
            });
        }
    });
    
    return results;
}

// Extract snippet around search term
function extractSnippet(content, query) {
    const index = content.indexOf(query);
    const start = Math.max(0, index - 50);
    const end = Math.min(content.length, index + query.length + 50);
    
    let snippet = content.substring(start, end);
    if (start > 0) snippet = '...' + snippet;
    if (end < content.length) snippet = snippet + '...';
    
    return snippet;
}

// Display search results
function displaySearchResults(results, container, query) {
    if (results.length === 0) {
        container.innerHTML = '<div class="no-results">Нічого не знайдено</div>';
        container.style.display = 'block';
        return;
    }
    
    const html = results.map(result => `
        <div class="search-result-item" data-section="${result.element.id}">
            <div class="result-title">${highlightText(result.title, query)}</div>
            <div class="result-snippet">${highlightText(result.snippet, query)}</div>
        </div>
    `).join('');
    
    container.innerHTML = html;
    container.style.display = 'block';
    
    // Add click handlers
    container.querySelectorAll('.search-result-item').forEach(item => {
        item.addEventListener('click', () => {
            const sectionId = item.dataset.section;
            const section = document.getElementById(sectionId);
            
            if (section) {
                section.scrollIntoView({ behavior: 'smooth', block: 'start' });
                container.style.display = 'none';
                document.getElementById('doc-search').value = '';
                
                // Highlight the section
                section.classList.add('highlighted');
                setTimeout(() => {
                    section.classList.remove('highlighted');
                }, 2000);
            }
        });
    });
}

// Highlight search term in text
function highlightText(text, query) {
    const regex = new RegExp(`(${query})`, 'gi');
    return text.replace(regex, '<mark>$1</mark>');
}

// Generate table of contents
function generateTableOfContents() {
    const tocContainer = document.getElementById('table-of-contents');
    if (!tocContainer) return;
    
    const headings = document.querySelectorAll('.docs-main h2, .docs-main h3');
    const toc = document.createElement('ul');
    toc.className = 'toc-list';
    
    let currentH2 = null;
    let currentH2List = null;
    
    headings.forEach(heading => {
        const id = heading.id || heading.textContent.toLowerCase().replace(/\s+/g, '-');
        heading.id = id;
        
        const link = document.createElement('a');
        link.href = `#${id}`;
        link.textContent = heading.textContent;
        link.className = 'toc-link';
        
        const li = document.createElement('li');
        li.appendChild(link);
        
        if (heading.tagName === 'H2') {
            toc.appendChild(li);
            currentH2 = li;
            currentH2List = null;
        } else if (heading.tagName === 'H3' && currentH2) {
            if (!currentH2List) {
                currentH2List = document.createElement('ul');
                currentH2List.className = 'toc-sublist';
                currentH2.appendChild(currentH2List);
            }
            currentH2List.appendChild(li);
        }
        
        // Smooth scroll
        link.addEventListener('click', (e) => {
            e.preventDefault();
            heading.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
    });
    
    tocContainer.appendChild(toc);
}

// Debounce function for search
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Add styles for search and other features
const docStyles = document.createElement('style');
docStyles.textContent = `
    /* Search Box */
    .doc-search {
        margin-bottom: 30px;
    }
    
    .search-box {
        position: relative;
        display: flex;
        align-items: center;
        background: var(--light-color);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 10px 15px;
        transition: var(--transition);
    }
    
    .search-box:focus-within {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
    }
    
    .search-box i {
        color: var(--text-color);
        margin-right: 10px;
    }
    
    .search-box input {
        flex: 1;
        border: none;
        background: none;
        outline: none;
        font-size: 0.95rem;
    }
    
    .search-box kbd {
        background: white;
        border: 1px solid var(--border-color);
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.75rem;
        color: var(--text-color);
    }
    
    /* Search Results */
    .search-results {
        display: none;
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: white;
        border: 1px solid var(--border-color);
        border-radius: 8px;
        margin-top: 10px;
        max-height: 400px;
        overflow-y: auto;
        box-shadow: var(--shadow-lg);
        z-index: 100;
    }
    
    .search-result-item {
        padding: 15px;
        border-bottom: 1px solid var(--border-color);
        cursor: pointer;
        transition: var(--transition);
    }
    
    .search-result-item:hover {
        background: var(--light-color);
    }
    
    .search-result-item:last-child {
        border-bottom: none;
    }
    
    .result-title {
        font-weight: 600;
        color: var(--dark-color);
        margin-bottom: 5px;
    }
    
    .result-snippet {
        font-size: 0.875rem;
        color: var(--text-color);
    }
    
    .result-snippet mark,
    .result-title mark {
        background: #fef3c7;
        color: inherit;
        padding: 2px 4px;
        border-radius: 2px;
    }
    
    .no-results {
        padding: 20px;
        text-align: center;
        color: var(--text-color);
    }
    
    /* Highlighted Section */
    .docs-section.highlighted {
        animation: highlight 2s ease;
    }
    
    @keyframes highlight {
        0%, 100% { background: transparent; }
        50% { background: #fef3c7; }
    }
    
    /* Line Numbers */
    .has-line-numbers {
        position: relative;
        padding-left: 60px !important;
    }
    
    .line-numbers {
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 50px;
        padding: 20px 0;
        background: rgba(0, 0, 0, 0.1);
        text-align: center;
        user-select: none;
    }
    
    .line-numbers span {
        display: block;
        color: #718096;
        font-size: 0.875rem;
        line-height: 1.5;
    }
    
    /* Code Language Label */
    .code-language {
        position: absolute;
        top: 10px;
        left: 10px;
        background: rgba(255, 255, 255, 0.1);
        color: #a0aec0;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    /* Table of Contents */
    .toc-list {
        list-style: none;
        padding: 0;
    }
    
    .toc-list li {
        margin-bottom: 10px;
    }
    
    .toc-link {
        color: var(--text-color);
        text-decoration: none;
        transition: var(--transition);
    }
    
    .toc-link:hover {
        color: var(--primary-color);
        transform: translateX(5px);
        display: inline-block;
    }
    
    .toc-sublist {
        list-style: none;
        padding-left: 20px;
        margin-top: 10px;
    }
    
    .toc-sublist .toc-link {
        font-size: 0.9rem;
    }
`;
document.head.appendChild(docStyles);