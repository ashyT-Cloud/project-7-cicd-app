import os

from flask import Flask, jsonify

app = Flask(__name__)

APP_NAME = os.getenv("APP_NAME", "project-7-cicd-app")
APP_VERSION = os.getenv("APP_VERSION", "0.1.0")


@app.route("/")
def home():
    return jsonify(
        {
            "application": APP_NAME,
            "version": APP_VERSION,
            "message": "Project 7 CI/CD application v0.3.0 is running",
        }
    )


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


@app.route("/version")
def version():
    return jsonify(
        {
            "application": APP_NAME,
            "version": APP_VERSION,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
