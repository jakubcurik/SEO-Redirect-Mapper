import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# Slovník pro cachování obsahu stránek
_page_cache = {}


def get_page_content(url, timeout=10):
    # Kontrola, zda je obsah stránky již v cachování slovníku
    if url in _page_cache:
        return _page_cache[url]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.encoding = response.apparent_encoding
        response.raise_for_status()
        _page_cache[url] = response.text
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Chyba při získávání obsahu stránky {url}: {e}")
        return None


def extract_data_from_url(url, ignored_selectors=None):
    content = get_page_content(url)
    if not content:
        print(f"[CHYBA] URL {url} nevrátila žádný obsah!")
        return {}

    soup = BeautifulSoup(content, "html.parser")

    # Odstranění ignorovaných selektorů
    if ignored_selectors:
        for selector in ignored_selectors.split(","):
            for elem in soup.select(selector.strip()):
                elem.decompose()  # Odstraní elementy ze stromu dokumentu

    # Zde pokračuje zpracování stránky
    if soup.body is None:
        print(f"Varování: Stránka {url} neobsahuje tělo (body).")
        page_content = ""
    else:
        page_content = ' '.join(soup.body.get_text().split())

    data = {
        "slug": url.split("/")[-1],
        "meta_title": soup.title.string if soup.title else "",
        "meta_description": soup.find("meta", {"name": "description"}).attrs["content"] if soup.find("meta", {
            "name": "description"}) else "",
        "headings": ' '.join([tag.get_text().strip() for tag in soup.find_all(["h1", "h2", "h3"])]),
        "page_content": page_content,
        "image_alt": ' '.join([img.attrs["alt"] for img in soup.find_all("img", alt=True)[:5]])
    }

    return data


def process_urls(urls, ignored_selectors=None):
    def fetch_data(url):
        # Vytáhněte data pomocí funkce, která bere URL a ignorované selektory
        data = extract_data_from_url(url, ignored_selectors)
        # Přidejte URL do dat
        data['url'] = url
        return data

    with ThreadPoolExecutor(max_workers=10) as executor:
        # Zpracování každé URL v poolu threadů s přidáním URL do výsledků
        results = list(executor.map(fetch_data, urls))
    return results

