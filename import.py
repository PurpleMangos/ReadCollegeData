import os
import requests
import io
import pandas as pd
import fitz  # PyMuPDF

# Folder to save downloads (optional)
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
    try:
        with fitz.open(path) as doc:
            all_text = ""
            for page in doc:
                all_text += page.get_text()
        print(f"📄 PDF extracted from {os.path.basename(path)}:\n")
        print(all_text[:1000])  # Limit output for readability
    except Exception as e:
        print(f"❌ Error reading PDF {path}: {e}")

def handle_excel(path):
    try:
        df = pd.read_excel(path)
        print(f"📊 Excel data from {os.path.basename(path)}:\n")
        print(df.head())
    except Exception as e:
        print(f"❌ Error reading Excel {path}: {e}")

def process_file(path):
    if path.lower().endswith(".pdf"):
        handle_pdf(path)
    elif path.lower().endswith((".xlsx", ".xls")):
        handle_excel(path)
    else:
        print(f"⚠️ Unsupported file type: {path}")

def main():
    print("📥 Enter links to PDFs or Excel files (one per line). Type 'done' to finish:")
    urls = []
    while True:
        link = input("URL: ").strip()
        if link.lower() == "done":
            break
        urls.append(link)
    
    for url in urls:
        path = download_file(url)
        if path:
            process_file(path)

if __name__ == "__main__":
    main()