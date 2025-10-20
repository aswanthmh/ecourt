from flask import Flask, render_template, request
from scraper.scraper import scrape_ecourts

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    results = None
    if request.method == "POST":
        cnr_number = request.form.get("cnr_number")
        results = scrape_ecourts(cnr_number)
    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)




