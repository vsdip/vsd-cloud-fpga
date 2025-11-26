import os
import subprocess
from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = "change-this"  # for flash() messages

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(ROOT_DIR, "src")
BUILD_DIR = os.path.join(ROOT_DIR, "build")
NGROK_URL_FILE = os.path.join(BUILD_DIR, "ngrok_url.txt")

os.makedirs(BUILD_DIR, exist_ok=True)


def run_cmd(cmd, cwd=None):
    """Run shell command and return (success, output)."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            shell=True,
            text=True,
            capture_output=True
        )
        success = (result.returncode == 0)
        output = result.stdout + "\n" + result.stderr
        return success, output
    except Exception as e:
        return False, str(e)


def get_ngrok_url():
    if os.path.exists(NGROK_URL_FILE):
        with open(NGROK_URL_FILE, "r") as f:
            return f.read().strip()
    return ""


def save_ngrok_url(url):
    with open(NGROK_URL_FILE, "w") as f:
        f.write(url.strip())


@app.route("/", methods=["GET"])
def index():
    ngrok_url = get_ngrok_url()
    # We won’t embed the full Verilog editor here;
    # students can edit src/top.v in VS Code. This page just controls build & flash.
    return render_template("index.html", ngrok_url=ngrok_url, log="")


@app.route("/set_ngrok", methods=["POST"])
def set_ngrok():
    url = request.form.get("ngrok_url", "").strip()
    save_ngrok_url(url)
    flash("ngrok URL saved.")
    return redirect(url_for("index"))


@app.route("/build", methods=["POST"])
def build():
    # Use Makefile target
    success, output = run_cmd("make bit", cwd=ROOT_DIR)
    ngrok_url = get_ngrok_url()
    if success:
        flash("Build successful. Bitstream generated.")
    else:
        flash("Build failed. See log below.")
    return render_template("index.html", ngrok_url=ngrok_url, log=output)


@app.route("/build_and_program", methods=["POST"])
def build_and_program():
    ngrok_url = get_ngrok_url()
    if not ngrok_url:
        flash("ngrok URL is not set. Please set it first.")
        return redirect(url_for("index"))

    # 1) Build bitstream
    success, output = run_cmd("make bit", cwd=ROOT_DIR)
    if not success:
        flash("Build failed. See log below.")
        return render_template("index.html", ngrok_url=ngrok_url, log=output)

    bit_path = os.path.join(BUILD_DIR, "top.bin")
    if not os.path.exists(bit_path):
        flash("Bitstream top.bin not found after build.")
        return render_template("index.html", ngrok_url=ngrok_url, log=output)

    # 2) Send bitstream to local agent via ngrok
    try:
        with open(bit_path, "rb") as f:
            resp = requests.post(
                ngrok_url,
                data=f,
                headers={"Content-Type": "application/octet-stream"},
                timeout=120
            )
        program_log = f"Programming status: {resp.status_code}\n{resp.text}"
        flash("Build & Program triggered. See log below.")
        combined_log = output + "\n\n" + program_log
    except Exception as e:
        flash("Programming request failed. See log below.")
        combined_log = output + "\n\nError sending bitstream: " + str(e)

    return render_template("index.html", ngrok_url=ngrok_url, log=combined_log)


if __name__ == "__main__":
    # For local tests. In Codespaces, you’ll start this via the terminal:
    # python server/server.py
    app.run(host="0.0.0.0", port=8000, debug=True)

