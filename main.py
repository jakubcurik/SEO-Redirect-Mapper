import streamlit as st
import pandas as pd
import os
import csv
import re
from modules.url_checker import filter_active_urls
from modules.scraper import process_urls
from modules.comparator import compare_urls


def detect_delimiter(uploaded_file):
    sample = uploaded_file.read(1024).decode('utf-8')
    uploaded_file.seek(0)
    sniffer = csv.Sniffer()
    return sniffer.sniff(sample).delimiter if sniffer.has_header(sample) else ','


def load_data(label, uploaded_file):
    try:
        if uploaded_file.name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith('.tsv'):
            df = pd.read_csv(uploaded_file, delimiter='\t')
        else:
            delimiter = detect_delimiter(uploaded_file)
            df = pd.read_csv(uploaded_file, delimiter=delimiter)
        return df
    except Exception as e:
        st.error(f"Nedaří se načíst soubor: {e}")
        return None


def valid_url(url):
    return re.match(r'https?://(?:www\.)?(?:[-\w]+\.)([-\w\.]+)+(:\d+)?(/[\w/_\.#-]*(\?\S+)?)?$', url.strip()) is not None


def find_url_column(df):
    for col in df.columns:
        if df[col].apply(lambda x: valid_url(str(x))).mean() > 0.7:
            df.rename(columns={col: 'url'}, inplace=True)
            return 'url'
    return None


def save_urls_to_file(df, filename):
    os.makedirs('data', exist_ok=True)
    file_path = os.path.join('data', filename)
    df.to_csv(file_path, index=False)
    st.success(f"URL adresy se uložili do souboru {file_path}")


def load_urls_from_file(filename):
    file_path = os.path.join('data', filename)
    return pd.read_csv(file_path) if os.path.exists(file_path) else None


def process_data_flow(df_old, df_new):
    url_column_old = find_url_column(df_old)
    url_column_new = find_url_column(df_new)
    if url_column_old is None or url_column_new is None:
        st.error("Vypadá to, že jeden ze souborů neobsahuje URL adresy.")
        return False

    df_old_active = filter_active_urls(df_old, 'url')
    df_new_active = filter_active_urls(df_new, 'url')
    if df_old_active.empty or df_new_active.empty:
        st.error("Ani jedna adresa neobsahuje stav 200 (OK).")
        return False

    save_urls_to_file(df_old_active, 'old_urls.csv')
    save_urls_to_file(df_new_active, 'new_urls.csv')
    return True


def save_data_to_csv(data, filename):
    """Uloží data do CSV souboru v adresáři 'data'."""
    data_df = pd.DataFrame(data)
    data_df.reset_index(drop=True, inplace=True)  # Reset indexů
    data_df['comparison_string'] = data_df.apply(lambda x: f"{x['slug']} {x['meta_title']} {x['meta_description']} {x['headings']} {x['page_content']} {x['image_alt']}", axis=1)
    data_df = data_df[['url', 'comparison_string']]  # Vyber pouze potřebné sloupce
    os.makedirs('data', exist_ok=True)
    filepath = os.path.join('data', filename)
    data_df.to_csv(filepath, index=False)
    st.success(f"Data byla uložena do souboru {filepath}.")


def main():
    st.title('Redirect Mapping Tool')
    uploaded_old = st.file_uploader("Vyber soubor s původními URL adresami", type=['csv', 'tsv', 'xls', 'xlsx', 'txt'], key='old')
    uploaded_new = st.file_uploader("Vyber soubor s novými URL adresami", type=['csv', 'tsv', 'xls', 'xlsx', 'txt'], key='new')

    if uploaded_old and uploaded_new:
        df_old = load_data("staré URL adresy", uploaded_old)
        df_new = load_data("nové URL adresy", uploaded_new)

        if df_old is not None and df_new is not None:
            if st.button("Zkontrolovat a vyčistit URL adresy"):
                with st.spinner('Probíhá kontrola a čištění URL adres...'):
                    if process_data_flow(df_old, df_new):
                        st.session_state['data_ready'] = True
                        st.success('URL adresy jsou vyčištěny a uloženy.')

    if 'data_ready' in st.session_state and st.session_state['data_ready']:
        ignored_selectors = st.text_input("Chceš z analýzy podobnosti vyloučit nějaké CSS selektory? Zadej je sem (víc hodnot odděl čárkou):", key='ignored_selectors')
        if st.button("Stáhnout data ze všech URL adres a porovnat"):
            with st.spinner('Probíhá stahování dat a porovnání...'):
                df_old_active = load_urls_from_file('old_urls.csv')
                df_new_active = load_urls_from_file('new_urls.csv')
                if df_old_active is not None and df_new_active is not None:
                    old_data = process_urls(df_old_active['url'].tolist(), ignored_selectors)
                    new_data = process_urls(df_new_active['url'].tolist(), ignored_selectors)
                    save_data_to_csv(old_data, 'old_data.csv')  # Uložení old_data do souboru
                    save_data_to_csv(new_data, 'new_data.csv')  # Uložení new_data do souboru
                    results = compare_urls(load_urls_from_file('old_data.csv'), load_urls_from_file('new_data.csv'))
                    save_urls_to_file(results, 'redirect_map.csv')  # Uložení výsledků do souboru
                    st.success('Porovnání bylo dokončeno a data byla uložena.')
                    with open(os.path.join('data', 'redirect_map.csv'), 'rb') as f:
                        st.download_button('Stáhnout redirect mapu', f, file_name='redirect_map.csv')


if __name__ == "__main__":
    main()
