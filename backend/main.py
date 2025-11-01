from flask import Flask, request

app = Flask(__name__)


@app.route("/classifyText", methods=["POST"])
def classify():
        text = request.json.get("prompt")
        return f"prompt: {text}"


# @app.post("/generatePrompt")

# @app.post("/formatPrompt")
