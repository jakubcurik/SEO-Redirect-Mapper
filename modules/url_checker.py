# url_checker.py
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


def check_url_status(urls):
    with ThreadPoolExecutor(max_workers=20) as executor:
        future_to_url = {executor.submit(requests.head, url, allow_redirects=True, timeout=5): url for url in urls}
        results = {}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                response = future.result()
                results[url] = response.status_code
            except Exception as e:
                results[url] = None  # V případě chyby vrátíme None pro danou URL
        return results


def filter_active_urls(df, url_column):
    urls = df[url_column].tolist()
    url_statuses = check_url_status(urls)
    active_urls = [url for url, status in url_statuses.items() if status == 200]
    return df[df[url_column].isin(active_urls)]
