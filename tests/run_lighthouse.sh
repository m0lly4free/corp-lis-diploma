#!/bin/bash
# Запуск Lighthouse CI для анализа производительности

echo "🚀 Запуск Lighthouse CI..."

# Устанавливаем зависимости (если нужно)
npm install -g @lhci/cli@0.12.x

# Запускаем сбор и анализ
lhci autorun --config=./tests/performance/lighthouse.config.js

# Выводим результат
echo "✅ Анализ завершен. Отчет доступен по ссылке выше."