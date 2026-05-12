import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://localhost"  # Или http://localhost если тестируете без SSL

def fetch_url(url, index):
    start_time = time.time()
    try:
        # verify=False так как сертификат самоподписанный
        response = requests.get(url, timeout=5, verify=False)
        duration = time.time() - start_time
        return {
            "index": index,
            "url": url,
            "status": response.status_code,
            "time": duration,
            "success": True
        }
    except Exception as e:
        return {
            "index": index,
            "url": url,
            "status": 0,
            "time": 0,
            "success": False,
            "error": str(e)
        }

def run_load_test(url, total_requests=100, max_workers=50):
    print(f" Начинаем нагрузочное тестирование: {url}")
    print(f" Запросов: {total_requests}, Одновременных пользователей: {max_workers}")
    
    start_global = time.time()
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(fetch_url, url, i) for i in range(total_requests)]
        for future in as_completed(futures):
            results.append(future.result())

    end_global = time.time()
    total_time = end_global - start_global

    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]
    avg_time = sum(r["time"] for r in results) / len(results)
    rps = total_requests / total_time

    print("\n" + "="*30)
    print(f"✅ Успешно: {len(successful)}")
    print(f"❌ Ошибок: {len(failed)}")
    print(f"⏱ Общее время: {total_time:.2f} сек")
    print(f"🔥 Requests Per Second (RPS): {rps:.2f}")
    print(f"⏳ Среднее время ответа: {avg_time:.3f} сек")
    print("="*30)

    if rps >= 20 and len(failed) == 0:
        print("🎉 ТЕСТ ПРОЙДЕН: Система держит нагрузку!")
    else:
        print("⚠️ ВНИМАНИЕ: Система не выдержала нагрузку или есть ошибки.")

if __name__ == "__main__":
    # Тестируем API новостей (самое тяжелое)
    run_load_test(f"{BASE_URL}/api/news/", total_requests=100, max_workers=50)
    
    # Тестируем список услуг
    run_load_test(f"{BASE_URL}/api/services/", total_requests=100, max_workers=50)