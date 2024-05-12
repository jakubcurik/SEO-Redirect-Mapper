import pandas as pd
from polyfuzz import PolyFuzz
from polyfuzz.models import TFIDF


def load_csv(filepath):
    """Načte CSV soubor do DataFrame."""
    try:
        return pd.read_csv(filepath)
    except Exception as e:
        print(f"Chyba při načítání souboru {filepath}: {str(e)}")
        return pd.DataFrame()


def compare_urls(df_old, df_new):
    """Porovná dva DataFrames a vrací mapu přesměrování."""
    # Inicializace PolyFuzz modelu
    model = PolyFuzz(TFIDF())
    from_list = df_old['comparison_string'].tolist()
    to_list = df_new['comparison_string'].tolist()

    # Spuštění porovnání
    model.match(from_list, to_list)
    matches = model.get_matches()

    # Přidání URL k výsledkům na základě odpovídajícího textu
    matches['old_url'] = matches['From'].apply(lambda x: df_old[df_old['comparison_string'] == x]['url'].values[0] if x in df_old['comparison_string'].values else None)
    matches['new_url'] = matches['To'].apply(lambda x: df_new[df_new['comparison_string'] == x]['url'].values[0] if x in df_new['comparison_string'].values else None)

    return matches[['stara_url', 'nova_url', 'podobnost']]


def save_to_csv(df, filepath):
    """Uloží DataFrame do CSV souboru."""
    try:
        df.to_csv(filepath, index=False)
        print(f"Výsledky byly uloženy do souboru {filepath}.")
    except Exception as e:
        print(f"Chyba při ukládání souboru {filepath}: {str(e)}")


def main():
    # Načtení dat
    df_old = pd.read_csv('data/old_data.csv')
    df_new = pd.read_csv('data/new_data.csv')

    if not df_old.empty and not df_new.empty:
        results = compare_urls(df_old, df_new)
        print("Výsledky porovnání:")
        print(results)
    else:
        print("Některý z datových souborů je prázdný.")


if __name__ == "__main__":
    main()
