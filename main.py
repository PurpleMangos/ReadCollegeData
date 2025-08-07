import data_importer

def main():
    print("📥 Enter links to PDFs or Excel files (one per line). Type 'done' to finish:")
    urls = []
    while True:
        link = input("URL: ").strip()
        if link.lower() == "done":
            break
        urls.append(link)

    results = data_importer.process_urls(urls)

    for filetype, path, data in results:
        print(f"\n=== {path} ===")
        if filetype == "pdf":
            print(data[:1000])  # Print first 1000 characters of PDF text
        elif filetype == "excel":
            print(data.head())  # Print first 5 rows of Excel
        else:
            print("Could not process this file.")

if __name__ == "__main__":
    main()
