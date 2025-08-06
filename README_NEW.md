# 🚀 HR Integration System

![Status](https://img.shields.io/badge/status-production-green)
![Version](https://img.shields.io/badge/version-1.0-blue)
![Time Saved](https://img.shields.io/badge/time%20saved-85%25-success)
![License](https://img.shields.io/badge/license-MIT-blue)

> Автоматизація HR-процесів через інтеграцію TeamTailor, BambooHR, Notion та Slack

## ✨ Що це?

Комплексна система автоматизації, яка **синхронізує дані між 4 HR-платформами** в реальному часі, економлячи 85% часу HR-менеджера та усуваючи помилки ручного введення даних.

## 📊 Ключові метрики

| Метрика | До автоматизації | Після автоматизації | Покращення |
|---------|-----------------|-------------------|------------|
| **Час на процес** | 45-60 хв | 5-7 хв | **-85%** |
| **Помилки даних** | Часті | Рідкісні | **-80%** |
| **Системи для оновлення** | 3 вручну | 1 автоматично | **-67%** |
| **Час онбордингу** | 3 дні | 1 день | **-67%** |

## 🎯 Основні можливості

✅ **Повна синхронізація** між TeamTailor ↔ BambooHR ↔ Notion  
✅ **Автоматичне створення** співробітників при наймі  
✅ **Реальний час** - webhook-based інтеграція  
✅ **Slack повідомлення** про всі важливі події  
✅ **Єдине джерело правди** - кінець дублюванню даних  

## 🚀 Швидкий старт

```bash
# 1. Отримайте доступ до n8n
URL: https://viragamesinc.app.n8n.cloud

# 2. Перевірте активність workflows
- Scenario 1: Department Sync ✅
- Scenario 2: Job Requisition ✅  
- Scenario 3: Employee Creation ✅

# 3. Запустіть тестову синхронізацію
Execute Workflow → Department Sync
```

## 📚 Документація

### 🌐 [Повна документація доступна на GitHub Pages →](https://yourusername.github.io/bamboohr/)

Або відкрийте локально:
```bash
cd docs
python -m http.server 8000
# Відкрийте http://localhost:8000
```

### Швидкі посилання:
- 📖 [Інструкція встановлення](docs/setup.html)
- 🔧 [Технічна документація](docs/docs.html)
- ❓ [Вирішення проблем](docs/troubleshooting.html)
- 🏗️ [Архітектура системи](docs/index.html#architecture)

## 🛠️ Технічний стек

- **Автоматизація:** n8n workflows
- **ATS:** TeamTailor API
- **HRIS:** BambooHR API  
- **База знань:** Notion API
- **Повідомлення:** Slack Webhooks
- **Мови:** JavaScript (n8n), Python (тестування)

## 📁 Структура проекту

```
bamboohr/
├── docs/                 # 🌐 GitHub Pages сайт
│   ├── index.html       # Головна сторінка
│   ├── setup.html       # Інструкція встановлення
│   └── assets/          # CSS, JS, зображення
├── src/                 # 📦 Вихідний код
│   ├── n8n/            # n8n workflows (JSON)
│   └── *.py            # Python скрипти для тестування
└── README.md           # Цей файл
```

## ⚡ Три основні сценарії

### 1️⃣ Синхронізація департаментів
- **Запуск:** Щотижня або вручну
- **Час:** 1-2 хвилини
- **Результат:** Повна синхронізація структури між Notion ↔ TeamTailor

### 2️⃣ Створення вакансій
- **Запуск:** При створенні в Notion
- **Час:** 30 секунд
- **Результат:** Автоматичне створення requisition в TeamTailor

### 3️⃣ Найм співробітників
- **Запуск:** Webhook при статусі "Hired"
- **Час:** 2-3 хвилини
- **Результат:** Профіль в BambooHR з усіма даними

## 🔐 Необхідні доступи

Всі API ключі вже налаштовані в n8n. Вам потрібен лише доступ до:
- ✅ n8n instance
- ✅ Notion workspace  
- ✅ Slack канал #hr-automation

## 📈 Результати впровадження

```
БУЛО: Потрійне введення даних → СТАЛО: Єдине джерело правди
БУЛО: 45-60 хвилин на процес → СТАЛО: 5-7 хвилин
БУЛО: Постійні розбіжності → СТАЛО: 100% синхронізація
БУЛО: Ручні перевірки → СТАЛО: Автоматичні повідомлення
```

## 🤝 Підтримка

**При виникненні проблем:**
1. Перевірте [Troubleshooting Guide](docs/troubleshooting.html)
2. Перегляньте логи в n8n Executions
3. Перевірте Slack канал для повідомлень про помилки
4. Створіть Issue в цьому репозиторії

## 👥 Команда

**Розроблено для:** Vira Games  
**Автор:** Дубовик Кирило  
**Дата:** Січень 2025

## 📄 Ліцензія

MIT License - вільне використання та модифікація

---

<div align="center">
  
**[🌐 Відкрити документацію](https://yourusername.github.io/bamboohr/) | [📧 Підтримка](mailto:support@viragames.com) | [🐛 Повідомити про проблему](https://github.com/yourusername/bamboohr/issues)**

</div>