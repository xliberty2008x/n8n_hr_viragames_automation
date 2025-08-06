# 🌐 GitHub Pages Documentation Site

## 📖 Про сайт

Це статичний сайт з документацією для HR Integration System, оптимізований для GitHub Pages.

## 🚀 Як запустити на GitHub Pages

### Варіант 1: Через налаштування репозиторію

1. **Завантажте папку `docs/` у ваш GitHub репозиторій**
   ```bash
   git add docs/
   git commit -m "Add documentation site"
   git push origin main
   ```

2. **Увімкніть GitHub Pages:**
   - Перейдіть в Settings → Pages
   - Source: Deploy from a branch
   - Branch: main (або master)
   - Folder: `/docs`
   - Натисніть Save

3. **Дочекайтесь деплою (1-2 хв)**
   - Сайт буде доступний за адресою:
   - `https://yourusername.github.io/yourrepo/`

### Варіант 2: GitHub Actions (автоматичний деплой)

Створіть файл `.github/workflows/deploy-docs.yml`:

```yaml
name: Deploy Documentation

on:
  push:
    branches: [ main ]
    paths:
      - 'docs/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs
```

## 📁 Структура сайту

```
docs/
├── index.html           # Головна сторінка
├── setup.html          # Інструкція встановлення
├── docs.html           # Повна документація (потрібно створити)
├── troubleshooting.html # Вирішення проблем (потрібно створити)
├── _config.yml         # Налаштування GitHub Pages
├── assets/
│   ├── css/
│   │   ├── style.css   # Основні стилі
│   │   └── docs.css    # Стилі документації
│   ├── js/
│   │   ├── main.js     # Основний JavaScript
│   │   └── docs.js     # JavaScript для документації
│   └── img/
│       └── *.svg       # SVG іконки
└── README.md           # Ця інструкція
```

## 🎨 Особливості дизайну

- **Responsive Design** - адаптований для всіх пристроїв
- **Dark Mode Ready** - підготовлений для темної теми
- **Smooth Animations** - плавні анімації та переходи
- **Search Functionality** - пошук по документації (Ctrl+K)
- **Code Highlighting** - підсвітка синтаксису коду
- **Copy Code Buttons** - кнопки копіювання коду

## 🛠️ Локальний запуск для тестування

### Варіант 1: Простий HTTP сервер (Python)
```bash
cd docs
python -m http.server 8000
# Відкрийте http://localhost:8000
```

### Варіант 2: Live Server (VS Code)
1. Встановіть розширення "Live Server"
2. Правий клік на `index.html`
3. Виберіть "Open with Live Server"

### Варіант 3: Node.js
```bash
npx http-server docs -p 8080
# Відкрийте http://localhost:8080
```

## 📝 Додавання нового контенту

### Нова сторінка:
1. Створіть новий HTML файл в `docs/`
2. Використовуйте існуючу структуру як шаблон
3. Додайте посилання в навігацію

### Новий розділ документації:
1. Додайте секцію з унікальним `id`
2. Додайте посилання в sidebar
3. JavaScript автоматично підхопить навігацію

## 🔧 Налаштування

### Зміна кольорів:
Редагуйте CSS змінні в `assets/css/style.css`:
```css
:root {
    --primary-color: #4F46E5;
    --secondary-color: #7C3AED;
    /* ... */
}
```

### Зміна метаданих:
Редагуйте `_config.yml` для SEO налаштувань

## 📊 Аналітика (опціонально)

Додайте Google Analytics в `<head>` кожної сторінки:
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

## 🐛 Вирішення проблем

**Сайт не відображається:**
- Перевірте Settings → Pages → Source
- Дочекайтесь 5-10 хвилин після першого деплою
- Перевірте Actions tab на помилки

**Стилі не працюють:**
- Перевірте шляхи до CSS файлів
- Використовуйте відносні шляхи

**404 помилка:**
- Перевірте baseurl в `_config.yml`
- Для проектних сайтів: `/repository-name`

## 📧 Підтримка

При виникненні питань створіть Issue в репозиторії або зв'яжіться з розробником.

---

*Розроблено для Vira Games*  
*Автор: Дубовик Кирило*  
*Січень 2025*