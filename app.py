from flask import Flask, request, jsonify, send_from_directory
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
import os, datetime

from seo_fetcher import fetch_seo_data
from ai_generator import generate_blog_post

load_dotenv()

app = Flask(__name__, static_folder="static")
scheduler = BackgroundScheduler()

# ----------  ROUTES  -------------------------------------------------

# Serve the single‑page UI
@app.route("/")
def root():
    return send_from_directory(app.static_folder, "index.html")

# Manual generation endpoint
@app.route("/generate", methods=["GET"])
def generate():
    keyword = request.args.get("keyword", "").strip()
    if not keyword:
        return jsonify({"error": "Missing keyword parameter"}), 400

    seo_data = fetch_seo_data(keyword)
    blog_post = generate_blog_post(keyword, seo_data)

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"generated_posts/{keyword.replace(' ', '_')}_{ts}.md"
    os.makedirs("generated_posts", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(blog_post)

    return jsonify({"keyword": keyword, "seo_data": seo_data,
                    "saved_as": filename, "blog_post": blog_post})

# ----------  SCHEDULER  ----------------------------------------------

KEYWORDS = ["wireless earbuds"]

def scheduled_job():
    for kw in KEYWORDS:
        seo = fetch_seo_data(kw)
        post = generate_blog_post(kw, seo)
        path = f"generated_posts/{kw.replace(' ', '_')}_{datetime.date.today()}.md"
        os.makedirs("generated_posts", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(post)
        print(f"[{datetime.datetime.now()}] Auto‑post saved -> {path}")

scheduler.add_job(scheduled_job, "cron", hour=0)
scheduler.start()

if __name__ == "__main__":
    print("✨ Flask server with APScheduler running on http://localhost:5000")
    app.run(debug=True)
