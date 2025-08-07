import os
import requests
import pandas as pd
import fitz  # PyMuPDF

os.makedirs("downloads", exist_ok=True)

def download_file(url):
    filename = url.split("/")[-1].split("?")[0]
    file_path = os.path.join("downloads", filename)
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(file_path, "wb") as f:
            f.write(response.content)
        print(f"✅ Downloaded: {filename}")
        return file_path
    except Exception as e:
        print(f"❌ Failed to download {url}: {e}")
        return None

def handle_pdf(path):
    with fitz.open(path) as doc:
        all_text = ""
        for page in doc:
            all_text += page.get_text()
    return all_text

def handle_excel(path):
    df = pd.read_excel(path)
    return df

def process_file(path):
    if path.lower().endswith(".pdf"):
        text = handle_pdf(path)
        return ("pdf", text)
    elif path.lower().endswith((".xlsx", ".xls")):
        df = handle_excel(path)
        return ("excel", df)
    else:
        print(f"⚠️ Unsupported file type: {path}")
        return (None, None)

def process_urls(urls):
    results = []
    for url in urls:
        path = download_file(url)
        if path:
            filetype, data = process_file(path)
            results.append((filetype, path, data))
    return results
