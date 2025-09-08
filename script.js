// script.js
document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('link-container');
    const searchBox = document.getElementById('search-box');
    const categoryFilters = document.getElementById('category-filters');
    let allData = []; // This will store the master list of links

    /**
     * Renders a list of card items to the DOM.
     * @param {Array} items The array of link objects to render.
     */
    const renderCards = (items) => {
        container.innerHTML = '';
        if (items.length === 0) {
            container.innerHTML = '<p>没有找到匹配的链接。</p>';
            return;
        }

        items.forEach(item => {
            const card = document.createElement('a');
            card.className = 'card';
            const cardContent = document.createElement('div');
            cardContent.className = 'card-content';

            let iconHtml = '';
            if (item.icon) {
                iconHtml = `<img src="${item.icon}" alt="${item.name} icon" class="card-icon" onerror="this.style.display='none'">`;
            } else {
                const initial = item.name.charAt(0).toUpperCase();
                iconHtml = `<div class="card-icon card-initial">${initial}</div>`;
            }

            cardContent.innerHTML = `
                ${iconHtml}
                <div class="card-name">${item.name}</div>
            `;

            card.appendChild(cardContent);

            if (item.description) {
                card.addEventListener('click', (e) => {
                    e.preventDefault();
                    const confirmMessage = `${item.description}\n\nContinue？\n--------------- \n是否继续访问?`;
                    if (confirm(confirmMessage)) {
                        window.open(item.url, '_blank');
                    }
                });
            } else {
                card.href = item.url;
                card.target = '_blank';
            }

            container.appendChild(card);
        });
    };

    /**
     * Filters the master list based on search and category, then renders the result.
     */
    const filterAndRender = () => {
        const searchTerm = searchBox.value.toLowerCase();
        const activeCategory = categoryFilters.value;

        let filteredData = allData;

        if (activeCategory !== 'All') {
            filteredData = filteredData.filter(item => item.category === activeCategory);
        }

        if (searchTerm) {
            filteredData = filteredData.filter(item => item.name.toLowerCase().includes(searchTerm));
        }

        renderCards(filteredData);
    };

    // Main execution starts here
    fetch('config.json')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            allData = data;

            if (!allData || allData.length === 0) {
                container.innerHTML = '<p>配置文件中没有链接。</p>';
                return;
            }

            // 1. Populate the category dropdown
            const categories = ['All', ...new Set(allData.map(item => item.category).filter(Boolean))];
            categories.forEach(category => {
                const option = document.createElement('option');
                option.value = category;
                option.textContent = category;
                categoryFilters.appendChild(option);
            });

            // 2. Perform the initial render
            renderCards(allData);

            // 3. Add event listeners
            searchBox.addEventListener('input', filterAndRender);
            categoryFilters.addEventListener('change', filterAndRender);
        })
        .catch(error => {
            console.error('无法加载配置文件:', error);
            container.innerHTML = `<p style="color: #ff8a80;">加载配置文件时出错。请检查文件是否存在且格式正确。</p>`;
        });
});
