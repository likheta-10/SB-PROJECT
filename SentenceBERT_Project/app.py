from flask import Flask, render_template, request
from utils.similarity import get_similarity

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    similarity = None
    normalized = None

    if request.method == "POST":
        reference = request.form["reference"]
        student = request.form["student"]

        similarity, normalized = get_similarity(student, reference)

    return render_template(
        "index.html",
        similarity=similarity,
        normalized=normalized
    )

if __name__ == "__main__":
    app.run(debug=True)