import requests
import time

def test_page_load(url, expected_time=3.0):
    """Тест загрузки страницы"""
    start = time.time()
    try:
        response = requests.get(url, timeout=10)
        end = time.time()
        load_time = end - start
        
        if response.status_code == 200 and load_time <= expected_time:
            print(f"✅ {url} загружена за {load_time:.2f} сек (требуется ≤ {expected_time} сек)")
            return True
        else:
            print(f"❌ {url} ошибка: статус {response.status_code}, время {load_time:.2f} сек")
            return False
    except Exception as e:
        print(f"❌ {url} ошибка: {str(e)}")
        return False

def test_api_response(url, expected_time=0.3):
    """Тест API ответа"""
    start = time.time()
    try:
        response = requests.get(url, timeout=5)
        end = time.time()
        response_time = end - start
        
        if response.status_code == 200 and response_time <= expected_time:
            print(f"✅ {url} ответил за {response_time:.3f} сек (требуется ≤ {expected_time} сек)")
            return True
        else:
            print(f"❌ {url} ошибка: статус {response.status_code}, время {response_time:.3f} сек")
            return False
    except Exception as e:
        print(f"❌ {url} ошибка: {str(e)}")
        return False

# Запуск тестов
if __name__ == "__main__":
    print("Тестирование производительности...")
    
    # Тесты страниц
    test_page_load("http://localhost:8000/")
    test_page_load("http://localhost:8000/contacts/")
    
    # Тесты API
    test_api_response("http://localhost:8000/api/services/")
    test_api_response("http://localhost:8000/api/news/")