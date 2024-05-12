
# Nástroj na efektivní tvorbu redirect mapy

## Popis
Tento nástroj na redirect mapping vytvořený v Pythonu slouží především SEO specialistům a využijí ho při redesignu webů a e-shopů nebo při jakýchkoliv úpravách na větších webech, kdy dojde ke změně URL adres.

Zjednodušeně řečeno, pokud se změní URL adresa, musí se vytvořit přesměrování, aby daná stránka nezratila pozici ve výsledcích vyhledávání a aby nevyhazovala chybu 404 - Nenalezeno.

U malých webů se dá přesměrování vyřešit manuálně a nebo pokud se například mění jen doména, je tvorba redirect mapy velmi jednoduchá a dá se pro ni využít třeba Excel. V situaci, kdy se ale URL adresy mění více a není na první pohled z URL adresy jasné, co se na ní nachází, přichází na řadu řešení v podobě tohoto nástroje na redirect mapping.

Nástroj funguje na principu scrapingu dat ze strých i nových URL adres a porovnávání textových dat vůči sobě pomocí knihovny PolyFuzz za pomocí modelu TF-IDF.

## Klíčové vlastnosti
- **Automatizovaný scraping URL adres**: Nástroj načte staré i nové URL adresy a extrahuje důležitá data jako jsou meta tagy, nadpisy, alt popsiy obrázků a obsah stránky.
- **Inteligentní porovnání obsahu**: Používá TF-IDF model skrze knihovnu PolyFuzz pro efektivní porovnání obsahu starých a nových URL adres.
- **Vytvoření přesměrovací mapy**: Generuje CSV soubor s redirect mapou na základě míry podobnosti extrahovaného obsahu.
- **Streamlit UI**: Umožňuje uživateli ovládat nástroj přes webové rozhraní.

## Technologie
- Python
- Streamlit
- Pandas pro manipulaci s daty
- Requests a BeautifulSoup pro scraping
- PolyFuzz pro porovnávání textů

## Možnosti spuštění nástroje
- Spuštění webové aplikace
- Instalace ve vlastním vývovjovém prostředí na localhostu

## Spuštění webové aplikace
Spuštění hostované aplikace je ta nejrychlejší a nejjednoduší možnost, jak nsátroj spustit a začít používat.

Stačí přejít na tuto adresu: https://seo-redirect-mapper.streamlit.app/

## Instalace ve vlastním prostředí
Projekt vyžaduje Python 3.11 nebo novější. Doporučuju použít virtuální prostředí.

1. Naklonuj si repozitář:
   ```
   git clone https://github.com/vas-adresa/redirect-mapping-tool.git
   cd redirect-mapping-tool
   ```

2. Vytvoř virtuální prostředí a aktivuj ho:
   ```
   python -m venv .venv
   .venv\Scripts\activate  # Na Windows
   source .venv/bin/activate  # Na Unix nebo MacOS
   ```

3. Instaluj potřebné závislosti:
   ```
   pip install -r requirements.txt
   ```

## Jak nástroj používat
Spusť Streamlit pomocí následujícího příkazu:
```
streamlit run main.py
```
Webové rozhraní ti umožní nahrát CSV, TSV, XLS, XLSX nebo TXT soubory obsahující URL adresy a sledovat postup zpracování až po finální vygenerování redirect mapy.

### Krok za krokem
1. **Nahrání souborů**: Nahraj soubory obsahující staré a nové URL adresy. Script by měl v souboru sám najít sloupec obsahujícíc URL adresy.
2. **Zpracování a kontrola URL**: Nástroj ověří dostupnost URL a vyčistí soubory od adres, které vyhazují jiný stav než 200.
3. **Scraping a analýza**: Script stáhne data potřebná k analýze z původního i nového webu.
4. **Generování redirect mapy**: Na základě analýzy je vytvořena redirect mapa a nabídnuta ke stažení.
