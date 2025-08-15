from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

indexed_pages = {}

def crawl(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            text = soup.get_text()
            indexed_pages[url] = text
    except Exception as e:
        print("Error crawling:", e)

@app.route("/", methods=["GET", "POST"])
def index():
    query = request.form.get("query")
    results = []
    if query:
        for url, content in indexed_pages.items():
            if query in content:
                results.append(url)
    return render_template("index.html", results=results)

@app.route("/crawl", methods=["POST"])
def crawl_route():
    urls = [
        "https://zgh.wikipedia.org",
        "https://shi.wikipedia.org",
        "https://tmz.wikipedia.org",
    ]
    for url in urls:
        crawl(url)
    return "Crawling done!"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
