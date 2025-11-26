from flask import Flask, request
import subprocess
import tempfile

app = Flask(__name__)

@app.route("/flash", methods=["POST"])
def flash():
    bitstream = request.data
    if not bitstream:
        return "No bitstream received", 400

    with tempfile.NamedTemporaryFile(suffix=".bin", delete=False) as f:
        f.write(bitstream)
        bit_file = f.name

    # PROGRAMMING COMMAND → you can change to openFPGALoader if you want
    cmd = ["iceprog", bit_file]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except Exception as e:
        return f"Programming failed: {e}", 500

    if result.returncode != 0:
        return f"Programming error:\n{result.stdout}\n{result.stderr}", 500

    return f"Programming successful:\n{result.stdout}\n{result.stderr}", 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
