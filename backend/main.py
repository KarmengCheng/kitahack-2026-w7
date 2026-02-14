import os
import random
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
# CORS allows your Firebase frontend to talk to this Cloud Run backend safely
CORS(app) 

@app.route('/')
def home():
    return "Backend is alive! Go to /api/vibe to check the vibe."

@app.route('/api/vibe', methods=['GET'])
def vibe_check():
    # This simulates our AI or database logic
    vibes = [
        "AI says: You are crushing it! ",
        "AI says: Don't forget to hydrate! ",
        "AI says: Deployments are looking green! ",
        "AI says: Sleep is for the weak (just kidding, sleep is important) "
    ]
    return jsonify({"message": random.choice(vibes)})

if __name__ == "__main__":
    # Cloud Run injects the PORT environment variable automatically (usually 8080)
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)