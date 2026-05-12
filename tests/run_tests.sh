#!/bin/bash
set -e

echo "🧪 Запуск тестов для АО «Корпорация ЛИС»"
echo "=========================================="

# 1. Установка зависимостей
echo "📦 Установка тестовых зависимостей..."
pip install -r requirements-test.txt

# 2. Запуск тестов по категориям
echo -e "\n🔹 Модульные тесты (модели, формы, API)"
docker-compose exec web python manage.py test tests.unit --verbosity=1

echo -e "\n🔹 Интеграционные тесты"
docker-compose exec web python manage.py test tests.integration --verbosity=1

echo -e "\n🔹 Функциональные тесты"
docker-compose exec web python manage.py test tests.functional --verbosity=1

echo -e "\n🔹 Тесты безопасности"
docker-compose exec web python manage.py test tests.security --verbosity=1

echo -e "\n🔹 Тесты мобильной адаптивности"
docker-compose exec web python manage.py test tests.mobile --verbosity=1

# 3. Проверка статики (простая)
echo -e "\n🔹 Проверка оптимизации статики"
docker-compose exec web python manage.py test tests.performance.test_static --verbosity=1

# 4. Отчет о покрытии
echo -e "\n📊 Отчет о покрытии:"
docker-compose exec web coverage report || echo "⚠️  Покрытие не сгенерировано (опционально)"

echo -e "\n✅ Тестирование завершено!"