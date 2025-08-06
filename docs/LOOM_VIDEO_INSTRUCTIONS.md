# 🎥 Інструкція для додавання Loom відео

## Як додати ваше Loom відео на сайт:

### 1. Запишіть відео в Loom
- Покажіть всю систему в дії
- Продемонструйте 3 основні сценарії
- Покажіть Slack повідомлення та workaround для approval flow
- Рекомендована тривалість: 10-20 хвилин

### 2. Отримайте embed код
1. Відкрийте ваше відео на loom.com
2. Натисніть кнопку **Share**
3. Виберіть вкладку **Embed**
4. Скопіюйте код

### 3. Вставте код в файл `docs/index.html`

Знайдіть цей коментар (рядок ~316):
```html
<!-- Розкоментуйте та вставте ваш Loom embed код тут:
```

Замініть placeholder на ваш код:

#### ДО:
```html
<div class="video-placeholder">
    <i class="fas fa-play-circle"></i>
    <h3>Loom Video</h3>
    <p>Вставте сюди embed код з Loom:</p>
    <code>&lt;iframe src="https://www.loom.com/embed/YOUR_VIDEO_ID"&gt;&lt;/iframe&gt;</code>
    ...
</div>
<!-- Розкоментуйте та вставте ваш Loom embed код тут:
<div style="position: relative; padding-bottom: 56.25%; height: 0;">
    <iframe src="https://www.loom.com/embed/YOUR_VIDEO_ID" 
            frameborder="0" 
            webkitallowfullscreen 
            mozallowfullscreen 
            allowfullscreen 
            style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border-radius: 12px;">
    </iframe>
</div>
-->
```

#### ПІСЛЯ:
```html
<!-- Видаліть або закоментуйте placeholder -->
<!-- <div class="video-placeholder">...</div> -->

<!-- Вставте ваш реальний Loom embed -->
<div style="position: relative; padding-bottom: 56.25%; height: 0;">
    <iframe src="https://www.loom.com/embed/abc123def456" 
            frameborder="0" 
            webkitallowfullscreen 
            mozallowfullscreen 
            allowfullscreen 
            style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border-radius: 12px;">
    </iframe>
</div>
```

### 4. Збережіть та запушіть
```bash
git add docs/index.html
git commit -m "🎥 Add Loom video presentation"
git push
```

### 5. Перевірте результат
Через 2-3 хвилини відкрийте:
https://xliberty2008x.github.io/n8n_hr_viragames_automation/

## 📝 Що показати у відео:

### Вступ (1-2 хв)
- Привітання та представлення
- Короткий огляд проблеми яку вирішує система
- Показати метрики (85% економія часу)

### Демонстрація Сценарію 1 (3-4 хв)
- Показати Notion з департаментами
- Запустити синхронізацію в n8n
- Показати результат в TeamTailor
- Показати Slack повідомлення

### Демонстрація Сценарію 2 (4-5 хв)
- Створити вакансію в Notion
- Показати автоматичне створення в TeamTailor
- **ВАЖЛИВО:** Показати Slack повідомлення рекрутеру
- Продемонструвати як рекрутер встановлює approval flow

### Демонстрація Сценарію 3 (3-4 хв)
- Показати кандидата в TeamTailor
- Перевести на статус "Hired"
- Показати створення в BambooHR
- Показати фінальне Slack повідомлення

### Висновки (1-2 хв)
- Підсумувати переваги
- Показати економію часу
- Подякувати за увагу

## 🎬 Поради для запису:

1. **Підготуйте тестові дані** заздалегідь
2. **Відкрийте всі вкладки** перед записом
3. **Використовуйте zoom** для важливих деталей
4. **Говоріть чітко** та не поспішайте
5. **Покажіть workaround** для approval flow детально

## 💡 Альтернатива: YouTube

Якщо віддаєте перевагу YouTube:
1. Завантажте відео на YouTube
2. Отримайте embed код
3. Вставте аналогічно до Loom

---

*Після додавання відео видаліть цей файл інструкцій*