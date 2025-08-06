#!/bin/bash

# Скрипт для пушу на GitHub після створення репозиторію

echo "🚀 Підключення до GitHub репозиторію..."
echo ""
echo "Після створення репозиторію на GitHub, введіть ваше GitHub ім'я користувача:"
read -p "GitHub username: " username

# Додаємо remote
git remote add origin https://github.com/$username/bamboohr-integration.git

# Перейменовуємо гілку на main
git branch -M main

# Пушимо код
echo ""
echo "📤 Відправляю код на GitHub..."
git push -u origin main

echo ""
echo "✅ Готово! Тепер налаштуйте GitHub Pages:"
echo ""
echo "1. Перейдіть на https://github.com/$username/bamboohr-integration/settings/pages"
echo "2. Source: Deploy from a branch"
echo "3. Branch: main"
echo "4. Folder: /docs"
echo "5. Натисніть Save"
echo ""
echo "🌐 Через 2-3 хвилини сайт буде доступний за адресою:"
echo "   https://$username.github.io/bamboohr-integration/"
echo ""