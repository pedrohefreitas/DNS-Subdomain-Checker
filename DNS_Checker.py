import requests
import os
import concurrent.futures
from tqdm import tqdm

def read_wordlist(file_path):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print("[ERROR] ARQUIVO NÃO ENCONTRADO!.")
        return []

def validate_url(base_url):
    if not base_url.startswith("http://") and not base_url.startswith("https://"):
        base_url = "https://" + base_url
    return base_url.rstrip('/')

def check_subdomain(base_url, subdomain):
    url = f"{base_url.split('://')[0]}://{subdomain}.{base_url.split('://')[1]}"
    try:
        response = requests.head(url, timeout=5)
        if response.status_code < 400:
            return url
    except requests.RequestException:
        pass
    return None

def check_subdomains_concurrently(base_url, wordlist):
    found_links = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(check_subdomain, base_url, subdomain): subdomain for subdomain in wordlist}
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(wordlist), desc="Verificando subdomínios"):
            result = future.result()
            if result:
                found_links.append(result)
    return found_links

def main():
    print("DNS Subdomain Checker!")

    txt_files = [file for file in os.listdir() if file.endswith('.txt')]

    if not txt_files:
        print("[ERROR] Nenhum arquivo .txt encontrado no diretório atual")
        return

    print("Wordlists disponíveis:")
    for i, file in enumerate(txt_files, 1):
        print(f"[{i}] {file}")

    try:
        choice = int(input("Selecione a wordlist (número): "))
        wordlist_file = txt_files[choice - 1]
    except (ValueError, IndexError):
        print("[ERROR] Número Inválido.")
        return

    wordlist = read_wordlist(wordlist_file)
    if not wordlist:
        print("[ERROR] A wordlist selecionada está vazia ou não é possível ler o arquivo.")
        return

    base_url = input("Informe o url: ").strip()
    base_url = validate_url(base_url)

    print(f"Começando o DNS checker {base_url} com {len(wordlist)} linhas...")
    found_links = []

    with tqdm(total=len(wordlist), desc="Verificando subdomínios") as progress_bar:
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = {executor.submit(check_subdomain, base_url, subdomain): subdomain for subdomain in wordlist}
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    found_links.append(result)
                progress_bar.update(1)

    if found_links:
        print("\n[RESULTADOS] Encontrados os seguintes subdomínios válidos:")
        for link in found_links:
            print(link)
    else:
        print("\n[INFO] Nenhum subdomínio válido encontrado.")

if __name__ == "__main__":
    main()
