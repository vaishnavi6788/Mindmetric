from flask import Flask, render_template, request

app = Flask(__name__, template_folder="templates")


def calculate_score(answer):
    if answer is None or not answer.strip():
        return None

    value = answer.strip().lower()

    try:
        number = float(value)
        if 0 <= number <= 100:
            return round(number)
    except ValueError:
        pass

    scores = {
        "never": 100,
        "not at all": 100,
        "always": 20,
        "very often": 20,
        "often": 35,
        "frequently": 35,
        "sometimes": 60,
        "occasionally": 75,
        "rarely": 85,
        "not sure": 50,
        "no difficulty": 100,
        "no problem": 100,
        "mild difficulty": 70,
        "some difficulty": 60,
        "moderate difficulty": 45,
        "severe difficulty": 25,
        "yes": 60,
        "no": 85
    }

    for option, score in scores.items():
        if value == option:
            return score

    return 50


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/assessment")
def assessment():
    return render_template("assessment.html")


@app.route("/result", methods=["GET", "POST"])
def result():
    if request.method == "POST":
        age = request.form.get("age", "")
        education = request.form.get("education", "")
        memory = request.form.get("memory", "")
        attention = request.form.get("attention", "")
        language = request.form.get("language", "")
        text = request.form.get("text", "")

        memory_score = calculate_score(memory)
        attention_score = calculate_score(attention)
        language_score = calculate_score(language)

        available_scores = [
            score for score in [
                memory_score,
                attention_score,
                language_score
            ]
            if score is not None
        ]

        overall_score = (
            round(sum(available_scores) / len(available_scores))
            if available_scores else None
        )

        return render_template(
            "result.html",
            age=age,
            education=education,
            memory=memory,
            attention=attention,
            language=language,
            response_text=text,
            memory_score=memory_score,
            attention_score=attention_score,
            language_score=language_score,
            overall_score=overall_score
        )

    return render_template("result.html")


if __name__ == "__main__":
    app.run(debug=True)
