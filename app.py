from flask import Flask, render_template, request
from scanner import scan_url
from db import scans
from datetime import datetime

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/scan", methods=["POST"])
def scan():
    url = request.form["url"]
    results, score = scan_url(url)

    scans.insert_one({
        "url": url,
        "results": results,
        "score": score,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    return render_template("result.html", url=url, results=results, score=score)


@app.route("/history")
def history():
    data = list(scans.find().sort("_id", -1))
    return render_template("history.html", scans=data)


if __name__ == "__main__":
    app.run(debug=True)