from flask import Flask, request, render_template
import feedparser

app = Flask(__name__)
sources = {}
@app.route('/')
def index():
    articles = []
    for source,url in sources.items():
        f = feedparser.parse(url)
        entries = [(source,entry) for entry in f.entries if entry != {}]
        articles.extend(entries)
    articles = sorted(articles, key= lambda x:x[1].published_parsed, reverse=True)
    page = request.args.get('page',1, type=int)
    n_page = 5
    tot_art = len(articles)
    start = ( page-1 )*n_page
    end = start + n_page
    paginated = articles[start:end]
    return render_template('index.html', src=sources.keys(), articles=paginated , page = page, total_pages=tot_art//n_page+1)
@app.route('/search')
def search():
    articles = []
    query = request.args.get('q','').lower()
    src = request.args.get('src','').lower()
    for source,url in sources.items():
        f = feedparser.parse(url)
        entries = [(source,entry) for entry in f.entries]
        articles.extend(entries)
    result = []
    if query or src=="all" and query != "":
        for article in articles:
            if query in article[1].title.lower():
                result.append(article)
    elif src:
        query=src
        for article in articles:
            if src in article[0].lower():
                result.append(article)
    
    return render_template("search.html", articles=result, query=query, src=sources.keys())
@app.route('/new', methods=["GET","POST"])
def new():
    if request.method == "POST":
        source = request.form.get('src')
        url = request.form.get('url')
        if source and url:
            sources[source]=url
        else:
            pass
        print(source, url)

    return render_template('new.html', sources=sources)
@app.route('/remove', methods=["GET", "POST"])
def remove():
    src = request.form.get('src')
    del sources[src]
    return render_template('new.html', sources=sources)
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
